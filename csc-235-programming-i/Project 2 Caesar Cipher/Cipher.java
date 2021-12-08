/**
 * Cipher.java
 * 
 * Program to decipher messages encoded using a Caesar
 * cipher.
 * 
 * @author TVD, CGG, and Simon Swenson
 * CSCI 235, Wheaton College, Fall 2011
 * Project 2
 * 10 Sept 2011
 */

import java.util.Scanner;
import java.io.*;

public class Cipher {

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
        


	int distance = 0;
	String next = "";
        while(!next.equals("quit")) {
	    distance += 1;
	    String newMessage = "";
	    // Your code to shift the message one more letter goes here;
	    // make newMessage contain the shifted message.
	    char bufferChar = ' '; //new char to hold the current character being looked at
	    for (int i = 0; i < message.length(); i++) { //loop to iterate through every single character in the message string
	        bufferChar = message.charAt(i); //make bufferChar get the current character we're looking at
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
	    // At this point, newMessage is expected to be the shifted message.
	    System.out.println("distance "+distance);
            System.out.println(newMessage);
            System.out.println("Press enter to see the next option, type 'quit' to quit.");
	    message = newMessage;
            next = keyboard.nextLine().trim();
        }
    }

}
    
  

