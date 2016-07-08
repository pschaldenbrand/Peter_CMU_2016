

public class LogEntry
{
	public String rowNum;
	public String sampleName;
	public String transactionID;
	public String studentID;
	public String sessionID;
	public String time;
	public String timeZone;
	public String duration;
	public String studentResponseType;
	public String studentResponseSubtype;
	public String tutorResponseType;
	public String tutorResponseSubtype;
	public String levelAssignment;
	public String levelProblemSet;
	public String problemName;
	public String problemView;
	public String problemStartTime;
	public String stepName;
	public String attempts;
	public String isLastAttempt;
	public String outcome;
	public String selection1;
	public String selection2;
	public String action1;
	public String action2;
	public String input;
	public String feedback;
	public String feedbackClassification;
	public String helpLevel;
	public String totalNumHints;
	public String kcSingle;
	public String kcCategorySingle;
	public String kcUnique;
	public String kcCategoryUnique;
	public String school;
	public String className;
	public String cfCompletionHistory;
	public String cfStepID;
	public String cfToolEventTime;
	public String cfTutorEventTime;
	
	
	/* Full Constructor.  Takes the line of values separated by tabs */
	public LogEntry (String line){
		String [] tokens = line.split("\t");
		int i = 0;
		
		rowNum = tokens[i++];
		sampleName = tokens[i++];
		transactionID = tokens[i++];
		studentID = tokens[i++];
		sessionID = tokens[i++];
		time = tokens[i++];
		timeZone = tokens[i++];
		duration = tokens[i++];
		studentResponseType = tokens[i++];
		studentResponseSubtype = tokens[i++];
		tutorResponseType = tokens[i++];
		tutorResponseSubtype = tokens[i++];
		levelAssignment = tokens[i++];
		levelProblemSet = tokens[i++];
		problemName = tokens[i++];
		problemView = tokens[i++];
		problemStartTime = tokens[i++];
		stepName = tokens[i++];
		attempts = tokens[i++];
		isLastAttempt = tokens[i++];
		outcome = tokens[i++];
		selection1 = tokens[i++];
		selection2 = tokens[i++];
		action1 = tokens[i++];
		action2 = tokens[i++];
		input = tokens[i++];
		feedback = tokens[i++];
		feedbackClassification = tokens[i++];
		helpLevel = tokens[i++];
		totalNumHints = tokens[i++];
		kcSingle = tokens[i++];
		kcCategorySingle = tokens[i++];
		kcUnique = tokens[i++];
		kcCategoryUnique = tokens[i++];
		school = tokens[i++];
		className = tokens[i++];
		cfCompletionHistory = tokens[i++];
		cfStepID = tokens[i++];
		cfToolEventTime = tokens[i++];
		cfTutorEventTime = tokens[i++];
	}
	
	
}