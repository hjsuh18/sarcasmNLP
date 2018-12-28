Setting classpath for execution:
Compile SentimentAnalyzer.java :
java -cp "../corenlp/:." SentimentAnalyzer.java

Execute SentimentAnalyzer
java -cp "../corenlp/:." SentimentAnalyzer

Compile SentimentAnalyzerEntryPoint.java :
javac -cp "../corenlp/:.:../py4j-0.10.8.1/py4j-java/py4j0.10.8.1.jar" SentimentAnalyzerEntryPoint.java

Execute SentimentAnalyzerEntryPoint :
java -cp "../corenlp/:.:../py4j-0.10.8.1/py4j-java/py4j0.10.8.1.jar" SentimentAnalyzerEntryPoint
