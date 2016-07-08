import java.io.*;
import java.util.*;

public class CompareExports
{
	public static void main(String [] args) throws IOException
	{
		String fname1 = "";
		String fname2 = "";
		
		BufferedReader br1 = new BufferedReader(new FileReader(fname1));
		BufferedReader br2 = new BufferedReader(new FileReader(fname2));
		
		System.out.println("Rows in 2 that aren't in 1:");
		
		HashSet<String> rows1 = createHashSet(br1);
		
		br2.readLine();
		while(br2.read()){
			String row = br2.readLine();
			if( rows1.contains(row) == false ){
				System.out.println(row);
			}
		}
		br1.close();  br2.close();	rows1 = null;
		
		br1 = new BufferedReader(new FileReader(fname1));
		br2 = new BufferedReader(new FileReader(fname2));
		
		System.out.println("Rows in 1 that aren't in 2:");
		
		HashSet<String> rows2 = createHashSet(br2);
		
		br1.readLine();
		while(br1.ready()){
			String row = br1.readLine();
			if( rows2.contains(row) == false ){
				System.out.println(row);
			}
		}
		
	}
	public static HashSet<String> createHashSet(BufferedReader br)throws IOException{
		HashSet<String> hs = new HashSet<String>();
		br.readLine();	//first line is just header stuff
		while(br.ready()){
			hs.add(br.readLine());
		}
		return hs;
	}
}