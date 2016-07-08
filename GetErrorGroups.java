import java.io.*;
import java.util.*;

public class GetErrorGroups
{
	public static void main (String [] args) throws IOException
	{
		String fileName = "C:\\Users\\peter\\Desktop\\log_structures\\FractionData.txt";
		Log log = new Log( fileName );
		ArrayList<ArrayList<ArrayList<String>>> studentLogs = log.getStudentsLogs();
		ArrayList<String> stepNames = log.getStepNameArray();
		HashMap<String,HashMap<String,Double>> probabilities = new HashMap<String,HashMap<String,Double>>();
		
		int stepNameIndex = log.getStepNameIndex();
		int outcomeIndex = log.getOutcomeIndex();
		
		for( String givenStep : stepNames )		//todo; can make this so much more efficient
		{
			HashMap<String,Double> condProb = new HashMap<String,Double>();
			for( String conditionStep : stepNames )
			{
				double times = 0;
				double outOf = 0;
				for( int i = 0; i < studentLogs.size(); i++ )
				{
					ArrayList<ArrayList<String>> currStudent = studentLogs.get(i);
					boolean givenError = false;
					boolean conditionError = false;
					for( int j = 0; j < currStudent.size(); j++ )
					{
						ArrayList<String> entry = currStudent.get(j);
						if(entry.get(stepNameIndex).equals(givenStep) &&
							entry.get(outcomeIndex).equals("INCORRECT")){
								givenError = true;
						}
						if(entry.get(stepNameIndex).equals(conditionStep) &&
							entry.get(outcomeIndex).equals("INCORRECT")){
								conditionError = true;
						}
					}
					if( !givenError ){
						//nothing
					}
					else if( givenError && conditionError ){
						times++;
						outOf++;
					}
					else if( givenError && !conditionError ){
						outOf++;
					}
				}
				if( outOf > 0 ){
					condProb.put(conditionStep, new Double((times/outOf)+""));}
			}
			probabilities.put(givenStep, condProb);
		}
		//group the errors together
		//**right now just print the results to analyze them
		double [] binDividers = {0.0,0.2,0.4,0.6,0.8,1.0};
		ArrayList<ArrayList<String>> stepGroups = new ArrayList<ArrayList<String>>();
		Object[] givenNames = probabilities.keySet().toArray();
		for( int i = 0; i < givenNames.length; i++ ){
			HashMap<String,Double> hm = probabilities.get((String)givenNames[i]);
			Object[] condNames = hm.keySet().toArray();
			for( int j = 0; j < condNames.length; j++ ){
				String given = (String)givenNames[i];
				String cond = (String)condNames[j];
				Double value = probabilities.get(given).get(cond);
				System.out.println("Pr("+given+"|"+cond+") = "+value.toString());
			}
		}
	}
}