// SentimentAnalyzer entry point when using py4j

import py4j.GatewayServer;

public class SentimentAnalyzerEntryPoint {
	private SentimentAnalyzer sa;

	public SentimentAnalyzerEntryPoint() {
		sa = new SentimentAnalyzer();
	}

	public SentimentAnalyzer getSentimentAnalyzer() {
		return sa;
	}

	public static void main(String[] args) {
		GatewayServer gatewayServer = new GatewayServer(new SentimentAnalyzerEntryPoint());
		gatewayServer.start();
		System.out.println("Gateway Server Started");
	}
}