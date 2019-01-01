// Use Stanford CoreNLP's sentiment package to generate features for
// training ML model.
// Features: Subjective/Objective; Positive/Negative; Sentiment contrast
// How to deal with text that has multiple sentences?
// For now, I think just taking the average / max of contrasts of all sentences is fine
// Might be better to round the decimals to 2 decimal points, since ML algorithm might perform better
// or might train faster

import edu.stanford.nlp.ling.CoreAnnotations.*;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.util.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.sentiment.*;
import edu.stanford.nlp.neural.rnn.*;
import java.util.*;
import org.ejml.simple.SimpleMatrix;

public class SentimentAnalyzer {
	public StanfordCoreNLP pipeline;

	public SentimentAnalyzer() {
		// set up pipeline properties
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,parse,sentiment");

		// build pipeline
		pipeline = new StanfordCoreNLP(props);
	}

	private static void printSentimentTree(Tree sentiTree) {	
		if (sentiTree == null)
			return;

			// BFS down the tree to get sentiment scores of phrases within sentence
			// and their contrasts
		List<List<Tree>> levels = new LinkedList<List<Tree>>();
		List<Tree> current = new LinkedList<Tree>();
		current.add(sentiTree);

		while (!current.isEmpty()) {
			levels.add(current);
			List<Tree> next = new LinkedList<Tree>();

			for (Tree t : current) {
				Tree[] children = t.children();				
				if (children.length <= 1)
					continue;
				for (Tree child : children)
					next.add(child);
			}
			current = next;
		}

		int count = 0;
		for (List<Tree> level : levels) {
			System.out.printf("Level %d:\n", count);

			for (Tree t : level) {
				SimpleMatrix m = RNNCoreAnnotations.getPredictions(t);
				double score = matrixToScore(m);
				t.pennPrint();
				System.out.println(score);
			}
			count++;
		}
	}

	private static double round(double d) {
		return (double) Math.round(d * 100) / 100;
	}


	// Get expected sentiment score from SimpleMatrix that holds probabilities of sentiments
	private static double matrixToScore(SimpleMatrix m) {
		if (m == null) return 0.0;
		double total = 0.0;
		double[] data = m.getMatrix().data;
		for (int i = 0; i < 5; i++) {
			total = total + data[i] * i;
		}
		return total;
	}

	// Get the positivity of sentence using corenlp sentiment analyzer
	public double getPositivity(String text) {
		Annotation document = new Annotation(text);

		pipeline.annotate(document);	
		List<CoreMap> sentences = document.get(SentencesAnnotation.class);

		double total = 0.0;
		int count = 0;

		for (CoreMap sent : sentences) {	
			Tree sentiTree = sent.get(SentimentCoreAnnotations.SentimentAnnotatedTree.class);
			SimpleMatrix m = RNNCoreAnnotations.getPredictions(sentiTree);
			double sentimentScore = matrixToScore(m); 
			total += sentimentScore;
			count++;
		}

		return round(total / count);
	}

	// returns a double in range 0 - 4 representing sentiment score of sentences
	// 0: very negative, 1: negative, 2: neutral, 3: positive, 4: very positive

	// returns an array arr of length 3 
	// list[0]: whole sentence positivity score
	// list[1]: adjacent sentiment contrast score 	
	// list[2]: maximum phrase sentiment score
	// list[3]: minimum phrase sentiment score
	// list[4]: phrase sentiment contrast score
	public List<Double> getFeatures(String text) {
		List<Double> features = new LinkedList<Double>();

		Annotation document = new Annotation(text);		
		// annnotate the document
		pipeline.annotate(document);
		List<CoreMap> sentences = document.get(SentencesAnnotation.class);
		if (sentences == null)
			return null;

		// whole sentence positivity score
		double total = 0.0;
		int count = 0;
		double maxContrast = Double.MIN_VALUE;
		double max = Double.MIN_VALUE;
		double min = Double.MAX_VALUE;
		Tree maxTree = null;
		Tree minTree = null;
		Tree leftTree = null;
		Tree rightTree = null;

		for (CoreMap sent : sentences) {
			Tree sentiTree = sent.get(SentimentCoreAnnotations.SentimentAnnotatedTree.class);
			printSentimentTree(sentiTree);

			SimpleMatrix m = RNNCoreAnnotations.getPredictions(sentiTree);
			double sentimentScore = matrixToScore(m); 
			total += sentimentScore;
			count++;

			// BFS down the tree to get sentiment scores of phrases within sentence
			// and their contrasts
			Queue<Tree> q = new LinkedList<Tree>();
			q.add(sentiTree);
			while (!q.isEmpty()) {
				Tree subtree = q.remove();
				if (subtree == null)
					continue;

				// update max and min sentiment scores of phrases
				SimpleMatrix subtreeMatrix = RNNCoreAnnotations.getPredictions(subtree);
				double subtreeScore = matrixToScore(subtreeMatrix);
				if (subtreeScore < min) {
					min = subtreeScore;
					minTree = subtree;
				}
				if (subtreeScore > max) {
					max = subtreeScore;
					maxTree = subtree;
				}

				// get two children of current node
				Tree[] children = subtree.children();
				if (children.length <= 1)
					continue;

				// get sentiment score of two children and their contrast
				SimpleMatrix leftMatrix = RNNCoreAnnotations.getPredictions(children[0]);
				double leftScore = matrixToScore(leftMatrix);
				SimpleMatrix rightMatrix = RNNCoreAnnotations.getPredictions(children[1]);
				double rightScore = matrixToScore(rightMatrix);
				double diff = Math.abs(leftScore - rightScore);
				if (diff > maxContrast) {
					leftTree = children[0];
					rightTree = children[1];
					maxContrast = diff;
				}

				for (Tree t : children) 
					q.add(t);
			}
		}
		features.add(round(total / count));
		features.add(round(maxContrast));
		features.add(round(max));
		features.add(round(min));
		features.add(round(max - min));

		leftTree.pennPrint();
		rightTree.pennPrint();
		maxTree.pennPrint();
		minTree.pennPrint();	

		return features;
	}

	private static void printList(List<Double> l) {
		for (double v : l) {
			System.out.print(v + " ");
		}
		System.out.println();
	}

	public static void main(String[] args) {
		SentimentAnalyzer sa = new SentimentAnalyzer();

		Scanner sc = new Scanner(System.in);
		while (sc.hasNextLine()) {
			String ln = sc.nextLine();
			List<Double> features = sa.getFeatures(ln);
			printList(features);
		}
	}
}
