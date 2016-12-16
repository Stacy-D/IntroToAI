package com.sheremet.checkers.client;

import checkers.pojo.board.Board;
import checkers.pojo.step.Step;

public interface Solver {

	public Step solve(Board board);

}
