from survey import radioQ, lfQ, exportSurveyLss

qs = [
	radioQ( "Do you identify as extroverted or introverted?", "Ex", answers=[("Extroverted", "Ex"),("Introverted", "In"),("I don't identify as either","NA")] ),
	lfQ( "Have you always identified as such? Feel free to elaborate." ),
	lfQ( "Do you feel like you'd enjoy spending more time socially than you have in the last week, do you feel like you spend too much time socially, or do you have some other answer?", "WantMoreLess"),
	lfQ( "In the last week, have you interacted socially (for 15 minutes or more) with anyone new? How did you meet them?", "TriedToMeet"),
	lfQ( "Do you have a 'best friend', a person with whom you spend the great majority of your social time? How long have you known them? How much of that time were you best friends? If not how many people do you make sure to interact with on a weekly basis?", "HaveBestFriend" ),
	lfQ( "Are you often exhausted by social situations? Are you ever?", "ExhaustedSocialSituations"),
	lfQ( "Do you think you have time right now to sustain a new relationship with someone, where you meet regularly and interact?", "HaveTimeForNew" ),
	lfQ( "If you any great sources of data where lots of people are being asked questions like these, please list one or two in the box below.", "AnySuggestions"),
]

exportSurveyLss( qs, "output2.lss" )
