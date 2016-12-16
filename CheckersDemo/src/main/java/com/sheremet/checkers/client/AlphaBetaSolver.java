package com.sheremet.checkers.client;

import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import checkers.pojo.board.Board;
import checkers.pojo.checker.CheckerColor;
import checkers.pojo.step.Step;

public class AlphaBetaSolver implements Solver {
	private static final long LIMIT = 5000;
	private StepCollector stepCollector = new StepCollector();
	private Heuristic heuristics = new Heuristic();
	private int depth;
	public AlphaBetaSolver(int depth) {
		this.depth = depth;
	}
	@Override
	public Step solve(Board board) {
		long startTime = System.currentTimeMillis();
		Step step = alphaBeta(board, depth);
		if(step == null){
			step = stepCollector.getSteps(board, board.getTurnColor()).get(0).getKey();
		}
		System.out.println("Time:"+(System.currentTimeMillis()-startTime));
		return step;
	}

	private Step alphaBeta(Board board, int depth){
		Step bestMove = null;
		int alpha = Integer.MIN_VALUE;
		for(Entry<Step,Board> state: stepCollector.getSteps(board, board.getTurnColor())){
			if(board.get(board.getTurnColor().opposite()).isEmpty()) // 
				return state.getKey(); // this is the state which leads to the victory
			int result = minscore(state, depth-1, alpha, Integer.MAX_VALUE);
			if(result > alpha){
				alpha = result;
				bestMove= state.getKey();
				}
		}
		return bestMove;
	}
private int maxscore(Entry<Step,Board> state, int depth, int alpha,int beta){
	Board board = state.getValue();
	if(board.get(CheckerColor.BLACK).isEmpty()
			|| board.get(CheckerColor.WHITE).isEmpty())
		return alpha;
	if(depth <=0 ) //add check of terminal state
		return heuristics.rateBoard(board);
	List<Entry<Step, Board>> currentLevelSteps = stepCollector.getSteps(board, board.getTurnColor()) ;
	if (currentLevelSteps.isEmpty()){
		switch (board.getTurnColor()) {
		case BLACK:
			return 100;
		case WHITE:
			return -100;
		default:
			break;
		}
	}
	for(Entry<Step,Board> nextState: currentLevelSteps){
		int score = maxscore(nextState, depth-1, alpha, beta);
		alpha = Math.max(alpha, score);
		if(alpha >= beta)
			return beta;
		}
	return alpha;
}
		private int minscore(Entry<Step,Board> state, int depth, int alpha,int beta){
			Board board = state.getValue();
			if(board.get(CheckerColor.BLACK).isEmpty()
					|| board.get(CheckerColor.WHITE).isEmpty())
				return beta;
			if(depth <=0 ) //add check of terminal state
				return heuristics.rateBoard(board);
			List<Entry<Step, Board>> currentLevelSteps = stepCollector.getSteps(board, board.getTurnColor()) ;
			for(Entry<Step,Board> nextState: currentLevelSteps){
		    		int score = maxscore(nextState, depth-1, alpha, beta);
		    		beta = Math.min(beta, score);
		    		if(alpha >= beta)
		    			return alpha;
		    		}
		    	return beta;
		    }
	}

	