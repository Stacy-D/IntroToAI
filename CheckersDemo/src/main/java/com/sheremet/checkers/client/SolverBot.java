package com.sheremet.checkers.client;

import checkers.client.CheckersBot;
import checkers.pojo.board.Board;
import checkers.pojo.checker.CheckerColor;
import checkers.pojo.step.Step;
import edu.princeton.cs.introcs.StdDraw;

public class SolverBot implements CheckersBot{
	private String name;
	private BoardRenderer renderer;
	private Solver solver;
	private CheckerColor color;
	public SolverBot(String name, BoardRenderer renderer, Solver solver) {
		this.name=name;
		this.renderer = renderer;
		this.solver = solver;
	}
	public void onGameStart(CheckerColor checkerColor) {
		color = checkerColor;
		System.out.println(checkerColor);
	}

	public Step next(Board board) {
		if (board.getTurnColor()!=color){
			throw new IllegalArgumentException();
		}
		Step finalStep = solver.solve(board);
		board.apply(finalStep);
		System.out.println(finalStep );
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		return finalStep;
	}
	/**
	 * Ends the game with message
	 * @param msg - message on the game ends
	 */
	public void onGameEnd(String msg) {
		renderer.showMsg(msg);
		System.out.println(msg);
	}

	public String clientBotName() {
		return name;
	}
	public void show(Board board) {
		renderer.render(board);
	}
	
}
