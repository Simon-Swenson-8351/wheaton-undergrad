/**
 * CipherAuto.java
 * 
 * Program to decipher messages encoded using a Caesar
 * cipher and chooses the message that will most likely make sense.
 * 
 * @author TVD, CGG, and Simon Swenson
 * CSCI 235, Wheaton College, Fall 2011
 * Project 2
 * 10 Sept 2011
 */

import java.util.Scanner;
import java.io.*;

public class CipherAuto {

    public static void main(String[] args) {

        // encrypted text
        String message;  

        // input from keyboard
        Scanner keyboard = new Scanner(System.in);

        // -----------------------------------------------------------------
        // this section contains stuff we haven't covered yet. 
        // ------------------------------------------------------------------
        if (args.length > 0) {
            message = "";
            try {
                Scanner inputFile = new Scanner(new File(args[0]));
                while(inputFile.hasNext()) 
                    message += inputFile.nextLine();
            } catch(IOException ioe) {
                System.out.println("File not found: " + args[0]);
                System.exit(-1);
            }
        }
        else {
            System.out.print("Please enter text--> ");
            message = keyboard.nextLine(); 
        }
        // ---------------------------------------------------------------------
        


	String next = "";
	String newMessage = "";
	char bufferChar = ' '; //new char to hold the current character being looked at
	String[] messages = new String[26]; //holds all 26 of the cipher cases for easy access
	int closenessToBest = 0; //the user will be able to go down the list from most likely (in case the computer returns a non-english phrase for the most likely). This int value determines how "close" the string is to the "best" as determined by the computer
	messages[0] = message;
	for (int i = 1; i < messages.length; i++) { //loop to put each of the 26 cases into messages.
	    for (int j = 0; j < message.length(); j++) { //loop to iterate through every single character in the message string
	        bufferChar = messages[i - 1].charAt(j); //make bufferChar get the current character we're looking at
	        if (Character.isLetter(bufferChar)) { //we only change letters, so this if statement covers that case only
		    if (bufferChar == 'z') { //the following if and else if prepare z (and Z) to become the char before a (and A) for incrementing the char.
			bufferChar = (char)('a' - 1);
		    }
		    else if (bufferChar == 'Z') {
			bufferChar = (char)('A' - 1);
		    }
			bufferChar += (char)1; //moves char up a letter
		}
		newMessage += bufferChar; //append the char to the new string
	    }
	    messages[i] = newMessage;
	    newMessage = "";
	}
	messages = sortLikelihood(messages);
        while(!next.equals("quit")) {
	    // At this point, newMessage is expected to be the shifted message.
            System.out.println(messages[closenessToBest]);
            System.out.println("Is this the English phrase you were looking for? If not, hit enter to see the \"next best\" result, else type \"quit\" to exit.");
            next = keyboard.nextLine().trim();
	    closenessToBest++;
        }
    }

    //Sorts the messages based on how likely they are to be the correct English translation. First, the method goes through the String held at index i and gives it an int value to test the likelihood of the case. After all the iterations are finished, it sorts the strings in the array based on the int values of their corresponding int array likelihood. Then, the method returns the sorted array.
    //PRECONDITION: the input must be a string array. Usually, all elements in str will be the same length. It is best if this length is greater than 2-5, as some code remains untested at these lengths. The inputs should have some number letters in them, or the method will be unable to sort them.
    //POSTCONDITION: there should be a string array to be assigned to the method's return value.
    //@param Param str is the string array to be sorted.
    //@return The method returns an array of strings that has been sorted such that the most likely string to be English (assuming all are the same length) is first, and so on.
    //@exception If the argument is not a String[], the method will throw an exception.
    private static String[] sortLikelihood(String[] str) {
	String[] common = {"th", "he", "at", "st", "an", "in", "ea", "nd", "er", "en", "re", "nt", "to", "es", "on", "ed", "is", "ti", "the", "and", "tha", "hat", "ent", "ion", "for", "tio", "has", "edt", "tis", "ers", "res", "ter", "con", "ing", "men", "tho", "ll", "tt", "ss", "ee", "pp", "oo", "rr", "ff", "cc", "dd", "nn", "e ", "t ", "s ", "d ", "n ", "r ", "y ", " the ", " of ", " are ", " i ", " and ", " you ", " a ", " can ", " to ", " he ", " her ", " that ", " in ", " was ", " is ", " has ", " it ", " him ", " his "}; //common character sequences found in the English language
	String temp; //holds the first value to be exchanged in the sort
	int temp2; //holds the first value to be exchanged in the sort
	String[] temp3; //holds the split string segments to be counted
	int[] likelihood = new int[str.length]; //holds the likelihood values for each element in str
	for(int i = 0; i < str.length; i++) { //loop to iterate through every element of str
	    likelihood[i] = 0; //handy spot to initilize all elements of likelihood
	    for (int j = 0; j < common.length; j++) { //loop to iterate through every element of common
		temp3 = str[i].toLowerCase().split(common[j]); //since class String has a way to test if a substring occurs in a string (.contains()), but has no way of counting how many times it occurs, we improvise and use split with regular expression common[j], then count how many elements the split created.
		likelihood[i] += temp3.length - 1; //add the number of occurances of the regular expression. NOTE THAT THIS WILL RETURN 1 LESS IF THE STRING BEGINS (OR ENDS) WITH THE EXPRESSION common[j]. The code below attemps to fix this problem.
		int countBeginning = 0; //used as an aid to determine if str[i] ends or beings with the regular expression being tested
		int countEnd = 0; //used as an aid to determine if str[i] ends or beings with the regular expression being tested		
		for (int k = 0; k < common[j].length(); k++) { //determines if str[i] ends or beings with the regular expression being tested by iterating through each character in the regular expression against the characters at the respective spots in str[i] both in the beginning and end
		    if (common[j].charAt(k) == str[i].charAt(k))
			countBeginning++;
		    if (common[j].charAt(k) == str[i].charAt(str[i].length() - common[j].length() + k))
			countEnd++;
		}
		if (countBeginning == common[j].length()) //adds one to likelihood if the reg expression is at the beginning
		    likelihood[i]++;
		if (countEnd == common[j].length()) //adds one if the reg exp is at the end
		    likelihood[i]++;
	    }
	}
	for(int i = 0; i < likelihood.length; i++) //for every element in likelihood:
	{
	    for(int j = i + 1; j < likelihood.length; j++) { //compare each to the elements proceeding it
		if(likelihood[i] < likelihood[j]) { //if the bigger number is farther from the beginning of the array then the smaller number, switch them (and their str[] counterparts)
		    temp2 = likelihood[i];
		    temp = str[i];
		    likelihood[i] = likelihood[j];
		    str[i] = str[j];
		    likelihood[j] = temp2;
		    str[j] = temp;
		}
	    }
	}
	return str;
    }

}
    
  

