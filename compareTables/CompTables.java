import java.io.*;
import java.util.*;

public class CompTables
{	
	public static void main (String [] args) throws IOException
	{
		BufferedReader oldT = new BufferedReader(new FileReader("gill_period3.txt"));
		BufferedReader newT = new BufferedReader(new FileReader("updateNewData.txt"));
		
		HashMap<String,String> transToRow = new HashMap<String,String>();
		HashSet<String> newTrans = new HashSet<String>();
		
		ArrayList<String> oldColumns = new ArrayList<String>();
		ArrayList<String> newColumns = new ArrayList<String>();
		
		String [] firstLine = oldT.readLine().split("\t");
		for( int i = 0; i < firstLine.length; i++ ){
			//System.out.print(firstLine[i]+"\t");
			oldColumns.add(firstLine[i]);
		}
		//System.out.println();
		firstLine = newT.readLine().split("\t");
		for( int i = 0; i < firstLine.length; i++ ){
			newColumns.add(firstLine[i]);
		}
		
		int newTransInd = newColumns.indexOf("CF (orig_trans_id)");
		int oldTransInd = oldColumns.indexOf("Transaction Id");
		
		while(newT.ready()){
			String line = newT.readLine();
			String [] values = line.split("\t");
			String trans = values[newTransInd];
			newTrans.add(trans);
			transToRow.put(trans,line);
		}
		
		int [] outOf = new int[ oldColumns.size()];
		int [] score = new int[ oldColumns.size()];
		
		ArrayList<String> commonCols = new ArrayList<String>();
		for( int i = 0; i < newColumns.size(); i++ ){
			String col = newColumns.get(i);
			if(oldColumns.contains(col)){
				commonCols.add(col);
				//System.out.print(col+"\t");
			}
		}
		//System.out.println();
		
		while(oldT.ready()){
			String line = oldT.readLine();
			String [] values = line.split("\t");
			String trans = values[oldTransInd];
			if(!newTrans.contains(trans)){
				//System.out.println(line);
				continue;
			}
			String [] newRow = transToRow.get(trans).split("\t");
			
			int ind;
			for( int i = 0; i < commonCols.size(); i++ ){
				ind = oldColumns.indexOf(commonCols.get(i));
				if(ind >= values.length){continue;}
				//System.out.print( values[ind]+"\t");
			}
			//System.out.println();
			for( int i = 0; i < commonCols.size(); i++ ){
				ind = newColumns.indexOf(commonCols.get(i));
				if(ind >= newRow.length){continue;}
				//System.out.print( newRow[ind]+"\t");
			}
			//System.out.println("\n");
			
			for(int i = 0; i < oldColumns.size(); i++ ){
				String whatsCompared = oldColumns.get(i);
				int indForNew = newColumns.indexOf(whatsCompared);
				//System.out.println(whatsCompared);
				if(indForNew < 0){continue;}
				if(i >= values.length){continue;}
				String o = values[i];
				//System.out.println(indForNew+"\t"+newRow.length);
				if(indForNew >= newRow.length){continue;}
				String n = newRow[indForNew];
				if( n.equals("") || o.equals("")){continue;}
				if( n.length()<1 || o.length()<1){continue;}
				if( o.equalsIgnoreCase(n)){
					score[i]+=1;
				}
				outOf[i]+=1;
			}
		}
		for( int i = 0; i < outOf.length; i++ ){
			if( outOf[i] <= 0  ){continue;}
			double perc = 100*((double)score[i]/(double)outOf[i]);
			System.out.println(perc+"\t"+oldColumns.get(i)+ "\t"+ outOf[i]);
		}
	}
}