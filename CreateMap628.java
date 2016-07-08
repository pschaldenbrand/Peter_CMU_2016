import java.io.*;
import java.util.*;

public class CreateMap628
{	
	public static void main (String [] args) throws IOException
	{
		BufferedReader br = new BufferedReader(new FileReader("6.28_in_2012.txt"));
		HashMap<String,HashMap<String,String>> map = getMapping("problem_set.xml");
		
		ArrayList<String> columns = new ArrayList<String>();	//contains the names of columns/fields
		
		String firstLine = br.readLine();
		String[] columnNames = firstLine.split("\t");
		for( int i = 0; i < columnNames.length; i++ ){
			columns.add( columnNames[i] );
		}
		
		ArrayList<ArrayList<String>> rows = new ArrayList<ArrayList<String>>();
		
		while( br.ready() )
		{
			String line = br.readLine();
			String [] tokens = line.split("\t");
			ArrayList<String> singleRow = new ArrayList<String>(Arrays.asList(tokens));
			rows.add(singleRow);
		}
				
		int assigIndex = columns.indexOf("Level (Assignment)");
		int problemSetIndex = columns.indexOf("Level (ProblemSet)");
		int problemNameIndex = columns.indexOf("Problem Name");
		
		String prob_file;
		String assign;
		String probSet;
		String probName;
		String swf;
		
		//These keep track of map rows already made so you don't have repeat rows.
		ArrayList<String> uniqueAssignments = new ArrayList<String>();
		ArrayList<String> uniqueProblems = new ArrayList<String>();
		
		System.out.println("Problem Name\tLevel (Assignment)\tLevel (ProblemSet)\tBRD\tSWF");
		
		for( int i = 0; i < rows.size(); i++ ){
			ArrayList<String> singleRow = rows.get(i);
			
			assign = singleRow.get(assigIndex);
			probSet = singleRow.get(problemSetIndex);
			probName = singleRow.get(problemNameIndex);
			
			prob_file = getProblemFile(probName,map);
			swf = getStudentInterface(probName,map);
			
			if( uniqueAssignments.contains(assign) && uniqueProblems.contains(probName) )
				continue;
			
			uniqueAssignments.add(assign);
			uniqueProblems.add(probName);
			
			System.out.print(probName+"\t"+assign+"\t"+probSet+"\t");
			System.out.println("FinalBRDs\\"+prob_file+"\tFlash\\"+swf);	//edit directories here!
		}
		
	}
	public static HashMap<String,HashMap<String,String>> getMapping(String fn)throws IOException{
		BufferedReader br = new BufferedReader(new FileReader(fn));
		
		HashMap<String,HashMap<String,String>> ret = new HashMap<String,HashMap<String,String>>();
		
		while(br.ready()){
			String line = br.readLine();
			String [] tokens = line.split("\\s+");
			
			if( tokens.length < 2 )
				continue;
			if(!tokens[1].equals("<Problem"))
				continue;
		
			String probName = "";
			String swf = "";
			String brd = "";
			
			for( int i = 0; i < tokens.length; i++ ){
				String [] s = tokens[i].split("=");
				if( tokens[i].length() < 2 ){continue;}
				
				if( tokens[i].contains("name")){
					String word = s[1];
					while(true){	//to deal with problem names that have spaces
						if( word.charAt(word.length()-1) == '\"' ){
							probName = probName + word.replaceAll("\"","");
							break;
						}
						else{
							probName = probName + word.replaceAll("\"","");
							word = " "+tokens[i+1];
							i++;
						}
					}
				}	
				else if (tokens[i].contains("problem_file")){
					brd = s[1].replaceAll("\"","");
				}
				else if (tokens[i].contains("student_interface")){
					swf = s[1].replaceAll("\"","");
				}
			}
			
			HashMap<String,String> hm = new HashMap<String,String>();
			hm.put("brd",brd);
			hm.put("swf",swf);
			ret.put(probName,hm);
		}
		return ret;
	}
	public static String getProblemFile(String name,HashMap<String,HashMap<String,String>>map){
		return map.get(name).get("brd");
	}
	public static String getStudentInterface(String name,HashMap<String,HashMap<String,String>>map){
		return map.get(name).get("swf");
	}
}