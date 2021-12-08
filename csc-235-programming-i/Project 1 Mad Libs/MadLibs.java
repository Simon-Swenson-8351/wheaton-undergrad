/**
 *MadLibs.java
 *
 *This program takes input from the
 *user using the Scanner class and
 *uses the input strings to create
 *a "Mad Lib" type story.
 *
 *@author Simon Swenson
 *Wheaton College, CSCI 235, Fall 2011
 *03 Sept 2011 v0.1
 */
import java.util.Scanner; //imported for reading user input from keyboard

public class MadLibs {

    public static void main(String[] args) {

	//Variable declaration
	String[] input = new String[10]; //Holds all of the 10 user inputs
	Scanner keyboard = new Scanner(System.in); //Declares a new Scanner to check user input
	String article0 = "a"; //String used before input[0] (a or an)
	String article4 = "a"; //String used before input[4] (a or an)
	String article2 = "a"; //String used before input[2] (a or an)

	//Getting user input
	System.out.println("Welcome to my Mad Libs program! Please give us a few words to use in our story!");
	System.out.print("noun (creature) --> ");
	input[0] = keyboard.nextLine();
	input[0] = input[0].toLowerCase();
	System.out.print("proper name (male) --> ");
	input[1] = keyboard.nextLine();
	System.out.print("noun (singular object) --> ");
	input[2] = keyboard.nextLine();
	input[2] = input[2].toLowerCase();
	System.out.print("adjective (emotion) --> ");
	input[3] = keyboard.nextLine();
	input[3] = input[3].toLowerCase();
	System.out.print("adjective --> ");
	input[4] = keyboard.nextLine();
	input[4] = input[4].toLowerCase();
	System.out.print("noun (creature) --> ");
	input[5] = keyboard.nextLine();
	input[5] = input[5].toLowerCase();
	System.out.print("onomatopoeia (ex. \"Bam,\" \"Slush,\" etc) --> ");
	input[6] = keyboard.nextLine();
	input[6] = input[6].toLowerCase();
	System.out.print("noun (plural creature) --> ");
	input[7] = keyboard.nextLine();
	input[7] = input[7].toLowerCase();
	System.out.print("gerund (verb ending with -ing) --> ");
	input[8] = keyboard.nextLine();
	input[8] = input[8].toLowerCase();
	System.out.print("past tense verb --> ");
	input[9] = keyboard.nextLine();
	input[9] = input[9].toLowerCase();

	//Capitalizing each word of the proper name
	String[] temp3 = input[1].split(" "); //holds all of the split segments of the string
	input[1] = "";
	for(int i = 0; i < temp3.length; i++) {
	    String temp = temp3[i].charAt(0) + ""; //holds a character to be capitalized
	    temp = temp.toUpperCase();
	    String temp2 = temp3[i].substring(1); //holds the current word excluding the first letter
	    temp3[i] = temp + temp2 + " ";
	    if(i == temp3.length - 1) //avoids putting spaces after the proper name's completion
		temp3[i] = temp + temp2;
	    input[1] = input[1] + temp3[i];
        }

	//Checks to see if the first input starts with a vowel to determine using a or an.
	char inputSub0FirstLetter = input[0].charAt(0);
	if(inputSub0FirstLetter == 'a' || inputSub0FirstLetter == 'e' || inputSub0FirstLetter == 'i' || inputSub0FirstLetter == 'o' || inputSub0FirstLetter == 'u')
	    article0 = "an";

	//Checks to see if the fifth input starts with a vowel to determine using a or an.
	char inputSub4FirstLetter = input[4].charAt(0);
	if(inputSub4FirstLetter == 'a' || inputSub4FirstLetter == 'e' || inputSub4FirstLetter == 'i' || inputSub4FirstLetter == 'o' || inputSub4FirstLetter == 'u')
	    article4 = "an";

	//Checks to see if the third input starts with a vowel to determine using a or an.
	char inputSub2FirstLetter = input[2].charAt(0);
	if(inputSub2FirstLetter == 'a' || inputSub2FirstLetter == 'e' || inputSub2FirstLetter == 'i' || inputSub2FirstLetter == 'o' || inputSub2FirstLetter == 'u')
	    article2 = "an";

	String temp4 = input[6].charAt(0) + "";
	temp4 = temp4.toUpperCase() + input[6].substring(1); //Capitalizes input[6] for starting a sentence

	//Telling story.
	System.out.println("There once was " + article0 + " " + input[0] + " named " + input[1] + ". Unfortunately, ");
	System.out.println("he had a bit of a problem. He had no " + input[2] + ". All of " + input[1] + "'s ");
	System.out.println("friends had " + article2 + " " + input[2] + ", but he did not. This made " + input[1] + " ");
	System.out.println("very " + input[3] + ", so one day he decided to fix the problem. The ");
	System.out.println("mischevious " + input[0] + " decided to steal " + article2 + " " + input[2] + " from " + article4 + " ");
	System.out.println(input[4] + " " + input[5] + ". " + temp4 + ", " + input[6] +  " was the sound " + input[1] + " ");
	System.out.println("made as he snuck into the " + input[5] + "'s house. \"Hey!\" shouted the ");
	System.out.println(input[5] + ". " + input[1] + " had been caught in the act! Even the ");
	System.out.println("neighborhood " + input[7] + " gathered around, " + input[8] +", clearly distraught ");
	System.out.println("by " + input[1] + "'s actions. One even " + input[9] + "! Fortunately for ");
	System.out.println(input[1] + ", though, the " + input[4] + " " + input[5] + " decided to be ");
	System.out.println("gracious and let the " + input[0] + " off with just a warning, this time. ");
	System.out.println("\"But, remember. If you ever try to steal my " + input[2] + " again, ");
	System.out.println("there'll be hell to pay!\" warned the " + input[5] + ". " + input[1] + " ");
	System.out.println("eventually learned to live without having any " + input[2] + ", ");
	System.out.println("and the rest of his days were spent happily ever after.");
	System.out.println("The end!");

    }
}