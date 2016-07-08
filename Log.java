import java.io.*;
import java.util.*;

public class Log
{
	private ArrayList<String> columns;
	private ArrayList<ArrayList<String>> rows;
	
	
	public Log (String fileName) throws IOException
	{
		columns = new ArrayList<String>();
		rows = new ArrayList<ArrayList<String>>();
		
		BufferedReader br = new BufferedReader(new FileReader(fileName));
		this.addColumns( br.readLine() );
		while( br.ready() )
		{
			this.addEntry( br.readLine() );
		}
	}
	
	public void addColumns (String firstLine)
	{
		String[] columnNames = firstLine.split("\t");
		for( int i = 0; i < columnNames.length; i++ ){
			this.columns.add( columnNames[i] );
		}
	}
	
	public void addEntry (String line)
	{
		String [] tokens = line.split("\t");
		ArrayList<String> newEntry = new ArrayList<String>();
		for( int i = 0; i < tokens.length; i++ ){
			newEntry.add( tokens[i] );
		}
		this.rows.add( newEntry );
	}
	
	public ArrayList<String> getStepNameArray(){
		ArrayList<String> ret = new ArrayList<String>();
		ArrayList<String> curr;
		String stepName;
		int index = columns.indexOf("Step Name");
		for( int i = 0; i < rows.size(); i++ ){
			curr = rows.get(i);
			stepName = curr.get(index);
			if( !ret.contains(stepName) ){
				ret.add(stepName);
			}
		}
		return ret;
	}
	public ArrayList<ArrayList<ArrayList<String>>> getStudentsLogs (){
		ArrayList<String> allStudentIDs = new ArrayList<String>();
		int studentIndex = columns.indexOf("Anon Student Id");
		for( int i = 0; i < rows.size(); i++ ){		//todo; this can be made more efficient
			String sID = rows.get(i).get(studentIndex);
			if( allStudentIDs.contains(sID) == false ){
				allStudentIDs.add(sID);
			}
		}
		ArrayList<ArrayList<ArrayList<String>>> studentLogs = new ArrayList<ArrayList<ArrayList<String>>>();
		for( int i = 0; i < rows.size(); i++ ){
			//System.out.println("getiingindex"+rows.get(i).get(studentIndex));
			int index = allStudentIDs.indexOf( rows.get(i).get(studentIndex) );
			boolean test = true;
			if( studentLogs.size() > index ){
				if( studentLogs.get(index) != null ){
					test = false;
					//System.out.println(studentLogs.get(index));
				}
			}
			if( test ){
				studentLogs.add(index, new ArrayList<ArrayList<String>>());
			}
			//System.out.println(studentLogs.get(index));
			studentLogs.get(index).add( rows.get(i) ); 
		}
		return studentLogs;
	}
	public int getStepNameIndex(){
		return columns.indexOf("Step Name");
	}
	public int getOutcomeIndex(){
		return columns.indexOf("Outcome");
	}
}