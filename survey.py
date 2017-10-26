answerTemplate = """   <row>
    <qid><![CDATA[{qid}]]></qid>
    <code><![CDATA[{aCode}]]></code>
    <answer><![CDATA[{aText}]]></answer>
    <sortorder><![CDATA[{order}]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>"""


questionAttTemplate = """   <row>
    <qid><![CDATA[{qid}]]></qid>
    <attribute><![CDATA[{att}]]></attribute>
    <value><![CDATA[{val}]]></value>
   </row>"""

questionTemplate = """   <row>
    <qid><![CDATA[{qid}]]></qid>
    <parent_qid><![CDATA[{parent_qid}]]></parent_qid>
    <sid><![CDATA[{sid}]]></sid>
    <gid><![CDATA[{gid}]]></gid>
    <type><![CDATA[L]]></type>
    <title><![CDATA[{qCode}]]></title>
    <question><![CDATA[{qText}]]></question>
    <preg/>
    <help/>
    <other><![CDATA[N]]></other>
    <mandatory><![CDATA[{mandatory}]]></mandatory>
    <question_order><![CDATA[{order}]]></question_order>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
    <same_default><![CDATA[0]]></same_default>
    <relevance><![CDATA[1]]></relevance>
   </row>"""

fpointscaleTemplate = """   
   <row>
    <qid><![CDATA[{qid}]]></qid>
    <parent_qid><![CDATA[{parent_qid}]]></parent_qid>
    <sid><![CDATA[{sid}]]></sid>
    <gid><![CDATA[{gid}]]></gid>
    <type><![CDATA[5]]></type>
    <title><![CDATA[{qCode}]]></title>
    <question><![CDATA[{qText}]]></question>
    <preg/>
    <help><![CDATA[{qHelp}]]></help>
    <other><![CDATA[N]]></other>
    <mandatory><![CDATA[{mandatory}]]></mandatory>
    <question_order><![CDATA[{order}]]></question_order>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
    <same_default><![CDATA[0]]></same_default>
    <relevance><![CDATA[{relevanceEquation}]]></relevance>
   </row>
"""

longfreeTemplate = """   <row>
    <qid><![CDATA[{qid}]]></qid>
    <parent_qid><![CDATA[{parent_qid}]]></parent_qid>
    <sid><![CDATA[{sid}]]></sid>
    <gid><![CDATA[{gid}]]></gid>
    <type><![CDATA[T]]></type>
    <title><![CDATA[{qCode}]]></title>
    <question><![CDATA[{qText}]]></question>
    <preg/>
    <help><![CDATA[{qHelp}]]></help>
    <other><![CDATA[N]]></other>
    <mandatory><![CDATA[{mandatory}]]></mandatory>
    <question_order><![CDATA[{order}]]></question_order>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
    <same_default><![CDATA[0]]></same_default>
    <relevance><![CDATA[{relevanceEquation}]]></relevance>
   </row>"""


import string
from collections import defaultdict

class SafeDict(dict):
     def __missing__(self, key):
         return '{' + key + '}'

def safeFormat( x, d ):
	return string.Formatter().vformat(x, (), SafeDict( d ))

class answer:
	def __init__(self, aText="No answer text supplied", aCode="NA"):
		self.aText = aText
		self.aCode = aCode

	def fillLss( self, text ):
		print( text, self.aText, self.aCode )
		return safeFormat( text, {
			"aText": self.aText,
			"aCode": self.aCode
		} )

def order( l ):
	return [ safeFormat( l[i], {"order": str(i+1)} ) for i in range(len(l)) ]


class radioQ:
	def __init__(self, qText="No question text supplied", qCode="NA", 
			type="L", answers=[], mandatory = "N"):
		self.parent_qid = 0
		answers += [("I'd rather not say", "NTH")]
		self.answers = [ answer( x[0], x[1] ) for x in answers ]
		self.qCode = qCode
		self.type = type
		self.mandatory = mandatory
		self.qText = qText
		self.template = questionTemplate

	def fillAnswerLss( self, text ):
		return safeFormat( text, {
			"qid": self.qid
		})

	def answersLss( self ):
		answers = self.answers

		aRows = [ ans.fillLss( answerTemplate ) for ans in answers ]
		aRows = order( aRows )

		aRows = [ self.fillAnswerLss( row ) for row in aRows ]

		return aRows

	def questionLss( self ):
		sid = 965597
		qid = self.qid
		gid = 1
		qCode = self.qCode
		relevanceEquation = ""
		qText = self.qText
		mandatory = self.mandatory
		qOrder = 1
		qHelp = "Almost done"

		parent_qid = self.parent_qid

		return safeFormat( self.template, locals())

class pick5Question:
	def __init__( self, *args, **kwargs ):
		radioQ.__init__( self, *args, **kwargs )
		self.template = fpointscaleTemplate

class lfQ(radioQ):
	def __init__( self, *args, **kwargs ):
		radioQ.__init__( self, *args, **kwargs )
		self.template = longfreeTemplate

class ynQ(radioQ):
	def __init__(self, *args, **kwargs):
		kwargs['answers'] = [ ("Yes", "Y"), ("No","N"), ("I don't know","IDK") ]
		radioQ.__init__(self, *args, **kwargs)

class c5Q(radioQ):
	def __init__(self, *args, **kwargs):
		kwargs['answers'] = [
			answer( "Just one", 1 ),
			answer( "Two", 2 ),
			answer( "Three", 3 ),
			answer( "Four", 4 ),
			answer( "Five", 5 ),
			answer( "More than five", -1 ),
			answer( "I'm not sure", -2 ),
		]
		radioQ.__init__(self, *args, **kwargs)

def exportSurveyLss( questions, fn ):
	i = 1
	for q in questions:
		q.qid = i+0
		i += 1

	answersLss = []
	questionsLss = []
	for q in questions:
		answersLss += q.answersLss()
		questionsLss += [q.questionLss()]

	questionsLss = order( questionsLss )

	qAttsLss = [ safeFormat( questionAttTemplate, {
		"qid": q.qid,
		"att": "hide_tip",
		"val": 1
	} ) for q in questions ]

	fullLss = open('template.lss').read()
	fullLss = safeFormat( fullLss, {
		"answers": "\n".join( answersLss ),
		"questions": "\n".join( questionsLss ),
		"qAtts": "\n".join( qAttsLss ),
		"boldAtTop": "Thank you! Feel free to skip around and answer whatever questions you like",
		"welcomeText": """
	<b>social interaction:</b> Exchanging dialogue with another person for at least 15 minutes. This can be while playing a game, cooking, driving, whatever.<br>
	<b>relationship:</b> When two people interact socially with eachother on a more or less regular basis for at least one month.<br>
	"""
	} )

	open(fn, "wb").write(fullLss)

