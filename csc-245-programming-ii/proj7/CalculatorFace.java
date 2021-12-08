/**
 * CalculatorFace.java
 *
 * Interface CalculatorFace to model the buttons and screens of a calculator.
 *
 * @author Thomas VanDrunen
 * CS 245, Wheaton College, Spring 2007
 * Project 1
 * Jan 19, 2007
 */

import java.util.*;
import javax.swing.*;

public interface CalculatorFace {

    public static final char PLUS_MINUS =  177;

    /**
     * Print a string to the screen portion of the calculator face.
     * POSTCONDITION: The given string is displayed on the screen
     * @param display The String to be displayed.
     */
    public void writeToScreen(String display);

    /**
     * Get references to the buttons of this calculator in the following
     * order: 0 1 2 3 4 5 6 7 8 9 . {+/-} + - * / = C.
     * @return An iterator for the buttons on this calculator.
     */
    public Iterator<JButton> getButtons();

    /**
     * Get a reference to the button for a given character.
     * @param c A character for which this calculator has a button (for 
     * example, '1').
     * @return A reference to the button corresponding to the given 
     * character, null if none.
     */
    public JButton getButton(char c);

    /**
     * Set the size of the window.
     * @param width The new width of this component in pixels
     * @param height The new height of this component in pixels
     */
    public void setSize(int x, int y);

    /**
     * Set the location of the window
     * @param x - the x-coordinate of the new location's top-left corner
     * @param y - the y-coordinate of the new location's top-left corner 
     */
    public void setLocation(int x, int y);
}