import java.io.*;
import java.lang.StringBuilder;
public class ValidationCleanup {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		File file = new File("C:\\Users\\josep\\OneDrive\\Documents\\UniversityofWashington\\SeniorProject\\BrianValidation\\LEDValidation\\LedVal21.csv");
		File file2 = new File("C:\\Users\\josep\\OneDrive\\Documents\\UniversityofWashington\\SeniorProject\\BrianValidation\\LEDValidation\\LedVal0.csv");

		FileReader fileReader = new FileReader(file); 
		StringBuilder sb = new StringBuilder();
		char c = 0;
		int signedInt = 0;
		while(signedInt != -1) {
				signedInt = fileReader.read();
				 c = (char)signedInt;//Reads the file character by character
				 sb.append(c);
		}
		//System.out.println(sb.toString());
		for(int i = 0; i < sb.length(); i ++) {
			if(sb.charAt(i) == '\"'){
				sb.replace(i, i+1, "");
			}
			sb.replace(sb.length()-1, sb.length(), "");
		}
	     //System.out.println(sb.toString());
		   // creates the file
		file.createNewFile();
		     
		      // creates a FileWriter Object
		FileWriter writer = new FileWriter(file2); 
		     
		      // Writes the content to the file
		writer.write(sb.toString()); 
		writer.flush();
		writer.close();

		      // Creates a FileReader Object
		

	

	}
}