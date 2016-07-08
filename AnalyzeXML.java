import java.io.*;
import java.util.*;
import java.sql.*;

public class AnalyzeXML
{
	public static void main (String [] args) throws IOException
	{
		File dir = new File("messages");
    	for(File file: dir.listFiles()){
		//for( int j =0; j < 15; j++ ){
			BufferedReader br = new BufferedReader(new FileReader(file));
			br.readLine();
			long prevTime = 0;
			int line = 0;
			while(br.ready()){
				String time = "";
				String [] toks = br.readLine().split("<");
				for( int i = 0; i < toks.length; i++ ){
					if(toks[i].length() > 4 ){
						if( toks[i].substring(0,5).equals("Time>") ){
							time = toks[i];
						}
					}
				}
				if( time.equals("") ){continue;}
				time = time.substring(5,time.length());
				//System.out.println(time);
				toks = time.split("\\s+");
				time = toks[0]+" "+toks[1];
				Timestamp t = Timestamp.valueOf(time);
				long currTime = t.getTime();
				//System.out.println(currTime);
				if(prevTime != 0){
					if( currTime - prevTime < 0 ){
						System.out.print("ISSUE in replay_"+file.getName()+"\t");
						System.out.println("on line\t"+line);
						System.out.println(t.toString());
					}
				}
				prevTime = currTime;
				line++;
			}
		}
	}
}