package com.sheremet.checkers.client;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import javax.media.j3d.Link;

import checkers.pojo.board.Board;
import checkers.pojo.checker.Checker;
import checkers.pojo.checker.CheckerColor;
import checkers.pojo.step.Step;
import edu.princeton.cs.introcs.In;

public class MinimaxSolver implements Solver {

	private static final long LIMIT = 5000;
	private StepCollector stepCollector = new StepCollector();
	private Euristics euristics = new Euristics();
	private int depth;
	public MinimaxSolver(int depth) {
		this.depth = depth;
	}
	@Override
	public Step solve(Board board) {

		long startTime = System.currentTimeMillis();
		Step step =  findMiniMaxSolution(board, depth, LIMIT).getValue().get(0);
		System.out.println("Time:"+(System.currentTimeMillis()-startTime));
		return step;
	}
	private Map.Entry<Integer, List<Step>> findMiniMaxSolution(Board board, int depth, long limit){
		long endTime = System.currentTimeMillis()+ limit;
		List<Entry<Step, Board>> currentLevelSteps = stepCollector.getSteps(board, board.getTurnColor()) ;
		if (currentLevelSteps.isEmpty()){
			switch (board.getTurnColor()) {
			case BLACK:
				return new MyEntry<Integer, List<Step>>(100, new LinkedList<Step>());
			case WHITE:
				return new MyEntry<Integer, List<Step>>(-100, new LinkedList<Step>());
			default:
				break;
			}
		}
		System.out.println(board);
		System.out.println("Found "+currentLevelSteps.size()+"turns.");
		System.out.println("DEPTH: "+depth+"{");
		if (depth==1){
			Step bestStep = null;
			Integer miniMax = null;
			for(Entry<Step, Board> stepEntry:currentLevelSteps){
				Step step = stepEntry.getKey();
				Board newBoard = stepEntry.getValue();
				System.out.println(newBoard);
				if (miniMax==null){
					bestStep = step;
					miniMax = euristics.rateBoard(newBoard) ;
					System.out.println("Rating: "+miniMax);

				}else{
					Integer currentRate = euristics.rateBoard(newBoard) ;
					System.out.println("Rating: "+currentRate);
					if (board.getTurnColor()==CheckerColor.BLACK){
						if (currentRate < miniMax){
							System.out.println("BLACK MINIMAX FOUND");
							miniMax = currentRate;
							bestStep = step;
						}
					}else{
						if (currentRate > miniMax){
							System.out.println("WHITE MINIMAX FOUND");
							miniMax = currentRate;
							bestStep = step;
						}
					}
				}
				if (System.currentTimeMillis()>endTime)break;
			}
			LinkedList<Step> newList = new LinkedList<Step>();
			newList.add(bestStep);
			return new MyEntry<Integer, List<Step>>(miniMax, newList);
		}else{
			Entry<Integer,List<Step>> miniMax = null;
			Step step = null;
			for(Entry<Step, Board> stepEntry:currentLevelSteps){
				Board newBoard = stepEntry.getValue();
				System.out.println(newBoard);
				if (miniMax==null){
					step = stepEntry.getKey();
					miniMax = findMiniMaxSolution(newBoard, depth-1, limit/currentLevelSteps.size());
					System.out.println("Total rating: "+miniMax.getKey());
				}else{
					Entry<Integer,List<Step>> alter = findMiniMaxSolution(newBoard, depth-1,limit/currentLevelSteps.size());
					System.out.println("Total rating: "+alter.getKey());
					if (board.getTurnColor()==CheckerColor.BLACK){
						if (alter.getKey() < miniMax.getKey()){
							System.out.println("BLACK MINIMAX FOUND");
							miniMax = alter;
							step  = stepEntry.getKey();
						}
					}else{
						System.out.println(alter);
						System.out.println(miniMax);
						if (alter.getKey() > miniMax.getKey()){
							System.out.println("WHITE MINIMAX FOUND");
							miniMax = alter;
							step  = stepEntry.getKey();
						}
					}
				}
				if (System.currentTimeMillis()>endTime)break;
			}
			miniMax.getValue().add(0,step);
			System.out.println("} DEPTH: "+depth);
			return miniMax;
		}
	}
}
class MyEntry<K,V> implements Map.Entry<K,V>{
	private final K key;
	private V value;
	public MyEntry(K k, V v) {
		key = k;
		value = v;
	}

	@Override
	public K getKey() {
		return key;
	}

	@Override
	public V getValue() {
		return value;
	}

	@Override
	public V setValue(V value) {
		V oldValue = getValue();
		this.value = value;
		return oldValue;
	}

}
