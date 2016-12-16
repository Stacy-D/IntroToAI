package com.sheremet.checkers.client;

import java.util.stream.Collectors;

import checkers.pojo.board.Board;
import checkers.pojo.checker.Checker;

public class Euristics {
	public int rateBoard(Board board){
		return (int) board.getCheckers().stream().collect(Collectors.summarizingInt(checker->{
			int rate = this.rateChecker(checker);
			//System.out.print("rate: "+rate+" ");
			return rate;
		})).getSum();
	}
	private int rateChecker(Checker checker){
		switch (checker.getType()) {
		case QUEEN:
			switch (checker.getColor()) {
			case BLACK:
				return -5;
			case WHITE:
				return 5;
			}
		case SIMPLE:
			switch (checker.getColor()) {
			case BLACK:
				return -1;
			case WHITE:
				return 1;
			}
		default:
			throw new IllegalArgumentException();
		}
	}
}
