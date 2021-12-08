import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;

/**
 * Class Driver
 *
 * Driver application to test calculators made from objects of
 * types CalculatorFront and CalculatorBack.
 *
 * @author Thomas VanDrunen and Simon Swenson
 * CS 245, Wheaton College, Spring 2007
 * Project 1
 * Jan 19, 2007 
 */

public class Driver {

	/**
	 * The calculator display
	 */
	private static final CalculatorFace f = new ConcreteCalculatorFace();

	/**
	 * The saved field which will be added, subtracted, etc. to
	 */
	private static String savedField = "0";
	
	/**
	 * The field which is currently being modified by the program.
	 */
	private static String currentField = "0";

	/**
	 * State supertype to change functionality of buttons
	 * @author Simon Swenson
	 *
	 */
	private static class State {

		/**
		 * The ButtonListener object that this State belongs to
		 */
		protected ButtonListener buttonListener;

		/**
		 * The State subtype to denote a button which will currently do nothing.
		 * @author Simon Swenson
		 *
		 */
		public static class EmptyState extends State {

			/**
			 * Constructor. Empty.
			 */
			public EmptyState() {
			}

			/**
			 * Does nothing on execution.
			 */
			public void run() {

			}
		}
		
		/**
		 * A specialized AdderState which will set up the subroutine for the first operator.
		 * @author Simon Swenson
		 *
		 */
		public static class FirstAdderState extends AdderState {

			/**
			 * Constructor
			 * @param val The value that this AdderState will add.
			 */
			public FirstAdderState(String val) {
				super(val);
			}
			
			/**
			 * Concatinates to currentField, then sets up the first operators.
			 */
			public void run() {
				super.run();
				setFirstOperators();
				setDigitsToAdders();
			}
		}
		
		/**
		 * A specialized AdderState which will set up the subroutine for overwriting previous data
		 * (used after the equals sign is pressed in case a user wants to put in different values).
		 * @author Simon Swenson
		 *
		 */
		public static class OverwriteState extends AdderState {
			
			/**
			 * Constructor
			 * @param val The value that this AdderState will add.
			 */
			public OverwriteState(String val) {
				super(val);
			}

			/**
			 * Sets value to currentField, then starts over.
			 */
			@Override
			public void run() {
				currentField = value;
				setPlusMinus();
				f.writeToScreen(format(currentField));
				setFirstOperators();
				setDigitsToAdders();
				savedField = "0";
			}
		}

		/**
		 * State dictating that the currentField will be concatinated with an arbitrary value.
		 * @author Simon Swenson
		 *
		 */
		public static class AdderState extends State {

			/**
			 * Value to concatinate to currentField.
			 */
			String value;

			/**
			 * Constructor
			 * @param val The value that this AdderState will add.
			 */
			public AdderState(String val) {
				value = val;
			}

			/**
			 * Concatinates the currentField with value, then ensures the sign toggle will be active.
			 */
			public void run() {
				currentField += value;
				setPlusMinus();
				super.run();
			}
		}

		/**
		 * State to add a decimal to the currentField.
		 * @author Simon Swenson
		 *
		 */
		public static class DecimalState extends State {

			/**
			 * Concatinates a decimal to currentField, then ensures that the rest of the states
			 * are set to correct values.
			 */
			public void run() {
				currentField += ".";
				setDigitsToAdders();
				setPlusMinus();
				setFirstOperators();
				buttonListener.setState(new EmptyState());
				super.run();
			}

		}

		/**
		 * State to toggle to minus sign when the currentField is "plus" or positive.
		 * @author Simon Swenson
		 *
		 */
		public static class PlusState extends State {

			/**
			 * Concatinates the "-" sign to the currentField, then ensures that the next time the button
			 * is pressed the inverse occurs.
			 */
			public void run() {
				currentField = "-" + currentField;
				buttonListener.setState(new MinusState());
				super.run();
			}

		}

		/**
		 * State to toggle to plus sign when the currentField is "minus" or negative.
		 * @author Simon Swenson
		 *
		 */
		public static class MinusState extends State {

			/**
			 * Removes the assumed "-" from the front of the currentField, then ensures that the
			 * next time the button is pressed the inverse occurs.
			 */
			public void run() {
				currentField = currentField.substring(1, currentField.length());
				buttonListener.setState(new PlusState());
				super.run();
			}
		}
		
		/**
		 * Supertype which all operators will use for  continuity.
		 * @author Simon Swenson
		 *
		 */
		public static class OperatorState extends State {
			
			/**
			 * Evaluates based on the operation, then calls operationHelper.
			 */
			@Override
			public void run() {
				String newSaved = evaluate() + "";
				operationHelper(newSaved);
			}
			
			/**
			 * Evaluates the fields. By default, will return the currentField.
			 * @return The currentField's value.
			 */
			protected String evaluate() {
				return Double.parseDouble(currentField) + "";
			}
			
			/**
			 * Helper method which serves as a collection of many things that operations need to do.
			 * @param newSaved The String to set the savedField to.
			 */
			protected static void operationHelper(String newSaved) {
				savedField = newSaved;
				currentField = "0";
				resetPlusMinus();
				resetDecimal();
				f.writeToScreen(format(savedField));
			}
		}
		
		/**
		 * Special state which tweaks things slightly differently compared to AdditionState.
		 * @author Simon Swenson
		 *
		 */
		public static class FirstAdditionState extends OperatorState {
			
			/**
			 * Saves the currentField and then ensures the next operator (or equals sign) that is pressed
			 * will do the actual addition (mimicks real calculator function).
			 */
			@Override
			public void run() {
				super.run();
				additionHelper();
				setOperatorsAddition();
				setDigitsToAdders();
			}
			
		}
		
		/**
		 * Addition state which will evaluate the sum of savedField and currentField.
		 * @author Simon Swenson
		 *
		 */
		public static class AdditionState extends OperatorState {
			
			/**
			 * Evaluates the sum and then tweaks some of the other ActionListeners' states to mimic
			 * real calculator functionality.
			 */
			@Override
			public void run() {
				super.run();
				additionHelper();
				setDigitsToAdders();
			}

			/**
			 * Evaluates the sum.
			 */
			@Override
			protected String evaluate() {
				return (Double.parseDouble(savedField) + Double.parseDouble(currentField)) + "";
			}
			
		}
		
		/**
		 * Addition state which will evaluate the sum of savedField and currentField. This
		 * state has some things specific to the equals sign that must be tweaked.
		 * @author Simon Swenson
		 *
		 */
		public static class AdditionEqualsState extends OperatorState {
			
			/**
			 * Evaluates the sum and then tweaks some of the other ActionListeners' states to mimic
			 * real calculator functionality.
			 */
			@Override
			public void run() {
				super.run();
				additionHelper();
				setDigitsToOverwrite();
				setFirstOperators();
				currentField = savedField;
				buttonListener.setState(new EmptyState());
			}

			/**
			 * Evaluates the sum.
			 */
			@Override
			protected String evaluate() {
				return (Double.parseDouble(savedField) + Double.parseDouble(currentField)) + "";
			}
			
		}
		
		/**
		 * Special state which tweaks things slightly differently compared to SubtractionState.
		 * @author Simon Swenson
		 *
		 */
		public static class FirstSubtractionState extends OperatorState {
			
			/**
			 * Saves the currentField and then ensures the next operator (or equals sign) that is pressed
			 * will do the actual subtraction (mimicks real calculator function).
			 */
			@Override
			public void run() {
				super.run();
				subtractionHelper();
				setOperatorsSubtraction();
				setDigitsToAdders();
			}
			
		}
		
		/**
		 * Subtraction state which will evaluate the difference of savedField and currentField.
		 * @author Simon Swenson
		 *
		 */
		public static class SubtractionState extends OperatorState {
			
			/**
			 * Evaluates the difference and then tweaks some of the other ActionListeners' states to mimic
			 * real calculator functionality.
			 */
			@Override
			public void run() {
				super.run();
				subtractionHelper();
				setDigitsToAdders();
			}

			/**
			 * Evaluates the difference.
			 */
			@Override
			protected String evaluate() {
				return (Double.parseDouble(savedField) - Double.parseDouble(currentField)) + "";
			}
			
		}
		
		/**
		 * Subtraction state which will evaluate the difference of savedField and currentField. This
		 * state has some things specific to the equals sign that must be tweaked.
		 * @author Simon Swenson
		 *
		 */
		public static class SubtractionEqualsState extends OperatorState {
			
			/**
			 * Evaluates the difference and then tweaks some of the other ActionListeners' states to mimic
			 * real calculator functionality.
			 */
			@Override
			public void run() {
				super.run();
				subtractionHelper();
				setDigitsToOverwrite();
				setFirstOperators();
				currentField = savedField;
				buttonListener.setState(new EmptyState());
			}

			/**
			 * Evaluates the difference.
			 */
			@Override
			protected String evaluate() {
				return (Double.parseDouble(savedField) - Double.parseDouble(currentField)) + "";
			}
			
		}
		
		/**
		 * Special state which tweaks things slightly differently compared to MultiplicationState.
		 * @author Simon Swenson
		 *
		 */
		public static class FirstMultiplicationState extends OperatorState {
			
			/**
			 * Saves the currentField and then ensures the next operator (or equals sign) that is pressed
			 * will do the actual multiplication (mimicks real calculator function).
			 */
			@Override
			public void run() {
				super.run();
				multiplicationHelper();
				setOperatorsMultiplication();
				setDigitsToAdders();
			}
			
		}
		
		/**
		 * Multiplication state which will evaluate the product of savedField and currentField.
		 * @author Simon Swenson
		 *
		 */
		public static class MultiplicationState extends OperatorState {
			
			/**
			 * Evaluates the product and then tweaks some of the other ActionListeners' states to mimic
			 * real calculator functionality.
			 */
			@Override
			public void run() {
				super.run();
				multiplicationHelper();
				setDigitsToAdders();
			}
			
			/**
			 * Evaluates the product.
			 */
			@Override
			protected String evaluate() {
				return (Double.parseDouble(savedField) * Double.parseDouble(currentField)) + "";
			}
			
		}
		
		/**
		 * Multiplication state which will evaluate the product of savedField and currentField. This
		 * state has some things specific to the equals sign that must be tweaked.
		 * @author Simon Swenson
		 *
		 */
		public static class MultiplicationEqualsState extends OperatorState {
			
			/**
			 * Evaluates the product and then tweaks some of the other ActionListeners' states to mimic
			 * real calculator functionality.
			 */
			@Override
			public void run() {
				super.run();
				multiplicationHelper();
				setDigitsToOverwrite();
				setFirstOperators();
				currentField = savedField;
				buttonListener.setState(new EmptyState());
			}

			/**
			 * Evaluates the product.
			 */
			@Override
			protected String evaluate() {
				return (Double.parseDouble(savedField) * Double.parseDouble(currentField)) + "";
			}
			
		}
		
		/**
		 * Special state which tweaks things slightly differently compared to DivisionState.
		 * @author Simon Swenson
		 *
		 */
		public static class FirstDivisionState extends OperatorState {
			
			/**
			 * Saves the currentField and then ensures the next operator (or equals sign) that is pressed
			 * will do the actual division (mimicks real calculator function).
			 */
			@Override
			public void run() {
				super.run();
				divisionHelper();
				setOperatorsDivision();
				setDigitsToAdders();
			}
			
		}
		
		/**
		 * Division state which will evaluate the quotient of savedField and currentField.
		 * @author Simon Swenson
		 *
		 */
		public static class DivisionState extends OperatorState {
			
			/**
			 * Evaluates the quotient and then tweaks some of the other ActionListeners' states to mimic
			 * real calculator functionality.
			 */
			@Override
			public void run() {
				super.run();
				divisionHelper();
				setDigitsToAdders();
			}

			/**
			 * Evaluates the quotient.
			 */
			@Override
			protected String evaluate() {
				return (Double.parseDouble(savedField) / Double.parseDouble(currentField)) + "";
			}
			
		}
		
		/**
		 * Division state which will evaluate the quotient of savedField and currentField. This
		 * state has some things specific to the equals sign that must be tweaked.
		 * @author Simon Swenson
		 *
		 */
		public static class DivisionEqualsState extends OperatorState {
			
			/**
			 * Evaluates the product and then tweaks some of the other ActionListeners' states to mimic
			 * real calculator functionality.
			 */
			@Override
			public void run() {
				super.run();
				divisionHelper();
				setDigitsToOverwrite();
				setFirstOperators();
				currentField = savedField;
				buttonListener.setState(new EmptyState());
			}

			/**
			 * Evaluates the quotient.
			 */
			@Override
			protected String evaluate() {
				return (Double.parseDouble(savedField) / Double.parseDouble(currentField)) + "";
			}
			
		}
		
		/**
		 * Default super run command: print the currentField to the calculator face.
		 */
		public void run() {
			f.writeToScreen(format(currentField));
		}

		/**
		 * Sets this State's ButtonListener.
		 * @param The ButtonListener to use.
		 */
		public void setButtonListener(ButtonListener b) {
			buttonListener = b;
		}
		
		/**
		 * Specific helper which executes code that all AdditionStates use.
		 */
		private static void additionHelper() {
			((ButtonListener)f.getButton('=').getActionListeners()[0]).setState(new AdditionEqualsState());
		}
		
		/**
		 * Specific helper which executes code that all SubtractionStates use.
		 */
		private static void subtractionHelper() {
			((ButtonListener)f.getButton('=').getActionListeners()[0]).setState(new SubtractionEqualsState());
		}
		
		/**
		 * Specific helper which executes code that all MultiplicationStates use.
		 */
		private static void multiplicationHelper() {
			((ButtonListener)f.getButton('=').getActionListeners()[0]).setState(new MultiplicationEqualsState());
		}
		
		/**
		 * Specific helper which executes code that all DivisionStates use.
		 */
		private static void divisionHelper() {
			((ButtonListener)f.getButton('=').getActionListeners()[0]).setState(new DivisionEqualsState());
		}

	}

	/**
	 * ActionListener class which is specific to the buttons used on the calculator.
	 * These ButtonListeners have states attached to them which will determine their functionality.
	 * @author Simon Swenson
	 *
	 */
	private static class ButtonListener implements ActionListener {

		/**
		 * This ButtonListener's current state.
		 */
		State state;

		/**
		 * Constructor.
		 */
		public ButtonListener() {
			state = null;
		}

		/**
		 * Constructor
		 * @param s State to initialize as.
		 */
		public ButtonListener(State s) {
			state = s;
			state.setButtonListener(this);
		}

		/**
		 * The code that is executed when the button is pressed.
		 */
		@Override
		public void actionPerformed(ActionEvent e) {
			state.run();
		}

		/**
		 * Changes this ButtonListener's state to the one indicated.
		 * @param s The new state to reflect.
		 */
		public void setState(State s) {
			state = s;
			state.setButtonListener(this);
		}

	}

	/**
	 * Sets up the various ButtonListeners for the calculator buttons.
	 * @param args Command line arguments.
	 */
	public static void main(String[] args) {
		f.getButton('0').addActionListener(new ButtonListener());
		f.getButton('1').addActionListener(new ButtonListener());
		f.getButton('2').addActionListener(new ButtonListener());
		f.getButton('3').addActionListener(new ButtonListener());
		f.getButton('4').addActionListener(new ButtonListener());
		f.getButton('5').addActionListener(new ButtonListener());
		f.getButton('6').addActionListener(new ButtonListener());
		f.getButton('7').addActionListener(new ButtonListener());
		f.getButton('8').addActionListener(new ButtonListener());
		f.getButton('9').addActionListener(new ButtonListener());
		resetDigits();

		f.getButton('.').addActionListener(new ButtonListener());
		resetDecimal();

		f.getButton(CalculatorFace.PLUS_MINUS).addActionListener(new ButtonListener());
		resetPlusMinus();

		f.getButton('C').addActionListener(new ButtonListener(new State() {

			@Override
			public void run() {
				savedField= "0";
				currentField = "0";
				resetDigits();
				resetOperators();
				resetDecimal();
				f.writeToScreen("0.0");
			}

		}));

		f.getButton('+').addActionListener(new ButtonListener());
		f.getButton('-').addActionListener(new ButtonListener());
		f.getButton('*').addActionListener(new ButtonListener());
		f.getButton('/').addActionListener(new ButtonListener());
		resetOperators();

		f.getButton('=').addActionListener(new ButtonListener());
		resetEquals();

		f.writeToScreen(format(currentField));
	}

	/**
	 * Resets digits to their original state.
	 */
	private static void resetDigits() {
		((ButtonListener)f.getButton('0').getActionListeners()[0]).setState(new State.EmptyState());
		((ButtonListener)f.getButton('1').getActionListeners()[0]).setState(new State.FirstAdderState("1"));
		((ButtonListener)f.getButton('2').getActionListeners()[0]).setState(new State.FirstAdderState("2"));
		((ButtonListener)f.getButton('3').getActionListeners()[0]).setState(new State.FirstAdderState("3"));
		((ButtonListener)f.getButton('4').getActionListeners()[0]).setState(new State.FirstAdderState("4"));
		((ButtonListener)f.getButton('5').getActionListeners()[0]).setState(new State.FirstAdderState("5"));
		((ButtonListener)f.getButton('6').getActionListeners()[0]).setState(new State.FirstAdderState("6"));
		((ButtonListener)f.getButton('7').getActionListeners()[0]).setState(new State.FirstAdderState("7"));
		((ButtonListener)f.getButton('8').getActionListeners()[0]).setState(new State.FirstAdderState("8"));
		((ButtonListener)f.getButton('9').getActionListeners()[0]).setState(new State.FirstAdderState("9"));
	}
	
	/**
	 * Sets digits to their normal adder states.
	 */
	private static void setDigitsToAdders() {
		((ButtonListener)f.getButton('0').getActionListeners()[0]).setState(new State.AdderState("0"));
		((ButtonListener)f.getButton('1').getActionListeners()[0]).setState(new State.AdderState("1"));
		((ButtonListener)f.getButton('2').getActionListeners()[0]).setState(new State.AdderState("2"));
		((ButtonListener)f.getButton('3').getActionListeners()[0]).setState(new State.AdderState("3"));
		((ButtonListener)f.getButton('4').getActionListeners()[0]).setState(new State.AdderState("4"));
		((ButtonListener)f.getButton('5').getActionListeners()[0]).setState(new State.AdderState("5"));
		((ButtonListener)f.getButton('6').getActionListeners()[0]).setState(new State.AdderState("6"));
		((ButtonListener)f.getButton('7').getActionListeners()[0]).setState(new State.AdderState("7"));
		((ButtonListener)f.getButton('8').getActionListeners()[0]).setState(new State.AdderState("8"));
		((ButtonListener)f.getButton('9').getActionListeners()[0]).setState(new State.AdderState("9"));
	}
	
	/**
	 * Resets the decimal button to its original state.
	 */
	private static void resetDecimal() {
		((ButtonListener)f.getButton('.').getActionListeners()[0]).setState(new State.DecimalState());
	}
	
	/**
	 * Resets the +/- button to its original state.
	 */
	private static void resetPlusMinus() {
		((ButtonListener)f.getButton(CalculatorFace.PLUS_MINUS).getActionListeners()[0]).setState(new State.EmptyState());
	}
	
	/**
	 * Sets the +/- button to its functional state (initially it cannot be used because 0 = -0).
	 */
	private static void setPlusMinus() {
		((ButtonListener)f.getButton(CalculatorFace.PLUS_MINUS).getActionListeners()[0]).setState(new State.PlusState());
	}
	
	/**
	 * Resets the equals sign back to its original state.
	 */
	private static void resetEquals() {
		((ButtonListener)f.getButton('=').getActionListeners()[0]).setState(new State.EmptyState());
	}
	
	/**
	 * Resets the operators back to their original states.
	 */
	private static void resetOperators() {
		((ButtonListener)f.getButton('+').getActionListeners()[0]).setState(new State.EmptyState());
		((ButtonListener)f.getButton('-').getActionListeners()[0]).setState(new State.EmptyState());
		((ButtonListener)f.getButton('*').getActionListeners()[0]).setState(new State.EmptyState());
		((ButtonListener)f.getButton('/').getActionListeners()[0]).setState(new State.EmptyState());
	}
	
	/**
	 * Sets the operators so that they will act slightly differently because they are the first function
	 * to be used.
	 */
	private static void setFirstOperators() {
		((ButtonListener)f.getButton('+').getActionListeners()[0]).setState(new State.FirstAdditionState());
		((ButtonListener)f.getButton('-').getActionListeners()[0]).setState(new State.FirstSubtractionState());
		((ButtonListener)f.getButton('*').getActionListeners()[0]).setState(new State.FirstMultiplicationState());
		((ButtonListener)f.getButton('/').getActionListeners()[0]).setState(new State.FirstDivisionState());
	}
	
	/**
	 * Sets all operator buttons to do addition in response to a previous button press.
	 */
	private static void setOperatorsAddition() {
		((ButtonListener)f.getButton('+').getActionListeners()[0]).setState(new State.AdditionState());
		((ButtonListener)f.getButton('-').getActionListeners()[0]).setState(new State.AdditionState());
		((ButtonListener)f.getButton('*').getActionListeners()[0]).setState(new State.AdditionState());
		((ButtonListener)f.getButton('/').getActionListeners()[0]).setState(new State.AdditionState());
	}
	
	/**
	 * Sets all operator buttons to do subtraction in response to a previous button press.
	 */
	private static void setOperatorsSubtraction() {
		((ButtonListener)f.getButton('+').getActionListeners()[0]).setState(new State.SubtractionState());
		((ButtonListener)f.getButton('-').getActionListeners()[0]).setState(new State.SubtractionState());
		((ButtonListener)f.getButton('*').getActionListeners()[0]).setState(new State.SubtractionState());
		((ButtonListener)f.getButton('/').getActionListeners()[0]).setState(new State.SubtractionState());
	}
	
	/**
	 * Sets all operator buttons to do multiplication in response to a previous button press.
	 */
	private static void setOperatorsMultiplication() {
		((ButtonListener)f.getButton('+').getActionListeners()[0]).setState(new State.MultiplicationState());
		((ButtonListener)f.getButton('-').getActionListeners()[0]).setState(new State.MultiplicationState());
		((ButtonListener)f.getButton('*').getActionListeners()[0]).setState(new State.MultiplicationState());
		((ButtonListener)f.getButton('/').getActionListeners()[0]).setState(new State.MultiplicationState());
	}
	
	/**
	 * Sets all operator buttons to do division in response to a previous button press.
	 */
	private static void setOperatorsDivision() {
		((ButtonListener)f.getButton('+').getActionListeners()[0]).setState(new State.DivisionState());
		((ButtonListener)f.getButton('-').getActionListeners()[0]).setState(new State.DivisionState());
		((ButtonListener)f.getButton('*').getActionListeners()[0]).setState(new State.DivisionState());
		((ButtonListener)f.getButton('/').getActionListeners()[0]).setState(new State.DivisionState());
	}
	
	/**
	 * Sets the digit buttons to overwrite previous saved input. Used after the user hits the
	 * equals sign and immediately follows it by a digit input.
	 */
	private static void setDigitsToOverwrite() {
		((ButtonListener)f.getButton('0').getActionListeners()[0]).setState(new State.OverwriteState("0"));
		((ButtonListener)f.getButton('1').getActionListeners()[0]).setState(new State.OverwriteState("1"));
		((ButtonListener)f.getButton('2').getActionListeners()[0]).setState(new State.OverwriteState("2"));
		((ButtonListener)f.getButton('3').getActionListeners()[0]).setState(new State.OverwriteState("3"));
		((ButtonListener)f.getButton('4').getActionListeners()[0]).setState(new State.OverwriteState("4"));
		((ButtonListener)f.getButton('5').getActionListeners()[0]).setState(new State.OverwriteState("5"));
		((ButtonListener)f.getButton('6').getActionListeners()[0]).setState(new State.OverwriteState("6"));
		((ButtonListener)f.getButton('7').getActionListeners()[0]).setState(new State.OverwriteState("7"));
		((ButtonListener)f.getButton('8').getActionListeners()[0]).setState(new State.OverwriteState("8"));
		((ButtonListener)f.getButton('9').getActionListeners()[0]).setState(new State.OverwriteState("9"));
	}
	
	/**
	 * Formats a string to fit on the calculator face and look good.
	 * @param str The string to format.
	 * @return The correctly formatted string.
	 */
	private static String format(String str) {
		double db = Double.parseDouble(str);
		str = db +"";
		if(str.length() <= 15) return str;
		else if(!str.contains("E")){
			return str.substring(0, 15);
		}
		else {
			String estr = str.substring(str.indexOf("E"), str.length());
			String fstr = str.substring(0, 15-estr.length());
			return (fstr + estr);
		}
	}
}
