import java.io.*;
import java.util.*;

public class AnalyzeMessages
{
	public static void main(String [] args) throws IOException
	{
		BufferedReader br = new BufferedReader(new FileReader("Replay_1_yonew.log"));
		HashSet<String> std_id = new HashSet<String>();
		HashSet<String> sess_id = new HashSet<String>();
		HashSet<String> trans_id = new HashSet<String>();
		
		while(br.ready()){
			String line = br.readLine();
			String [] tokens = line.split("\\s+");
			
			for( int i = 0; i < tokens.length; i++ ){
				String s = tokens[i];
				if(s.contains("user_guid") ){
					String [] ar = s.split("=");
					System.out.println(ar[1]);
				}
				/*if( s.contains("session_id")){
					String [] ar = s.split("=");
					if(sess_id.contains(ar[1]) == false ){
						sess_id.add(ar[1]);}
					else{
						
					}
				}
				if( s.contains("user_guid")){
					String [] ar = s.split("=");
					if(std_id.contains(ar[1]) == false ){
						std_id.add(ar[1]);}
					else{
					}
				}*/
			}
			System.out.println("#sessions = "+sess_id.size());
			System.out.println("#users = "+std_id.size());
			System.out.println(std_id.toString());
		}
	}
}