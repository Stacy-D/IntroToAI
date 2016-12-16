package com.sheremet.checkers.client;

import java.awt.Point;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Map.Entry;

import checkers.pojo.board.Board;
import checkers.pojo.checker.Checker;
import checkers.pojo.checker.CheckerColor;
import checkers.pojo.checker.CheckerType;
import checkers.pojo.checker.Position;
import checkers.pojo.exceptions.DoOneMoreStepException;
import checkers.pojo.step.Step;
import checkers.pojo.step.StepUnit;
import checkers.utils.Validator;

public class StepCollector {
	private static final Point[] DIRECTIONS = {new Point(-1,-1),new Point(-1,1),new Point(1,-1),new Point(1, 1)};
	public List<Entry<Step,Board>> getSteps(Board origin, CheckerColor color){
		Board board = origin.clone();
		List<Entry<Step,Board>> list = new LinkedList<Entry<Step,Board>>();
		outer:for(Checker checker:origin.get(color)){
			int count=checker.getType()==CheckerType.SIMPLE?2:7;
			for(int d = 1; d<=count; d++){
				for(Point dir:DIRECTIONS){
					try{
						Position p = new Position(
								checker.getPosition().getX()+dir.x*d,
								checker.getPosition().getY()+dir.y*d);
						StepUnit stepUnit = new StepUnit(checker.getPosition(), p);
						Step step = new Step();
						step.addStep(stepUnit);
						if (new Validator().isValidStep(board, step, color)){
							try{
								board.apply(step);
							}catch(IllegalArgumentException e){
								if (e.getCause() instanceof DoOneMoreStepException){
									CheckerType type = checker.getType();
									if (type == CheckerType.SIMPLE){
										if (board.hasBecameQueen(color,stepUnit.getTo())){
											type = CheckerType.QUEEN;
										}
									}
									continueSteps(step,board,color,type);
								}else{
									throw e;
								}
							}
							//System.out.println(Arrays.deepToString(board.getCheckers().toArray()));
							list.add(new MyEntry<Step,Board>(step, board));
							board = origin.clone();
							continue;
						}
					}catch(IllegalArgumentException e){ }
				}
			}
		}
		return list;
	}
	private void continueSteps(Step step, Board board, CheckerColor color, CheckerType type) {
		outer:while(true){
			int count = 2;
			if (type==CheckerType.QUEEN){
				count = 7;
			}
			for(int d = 1; d<=count; d++){
				for(Point dir:DIRECTIONS){
					try{
						Position def = step.getSteps().get(step.getSteps().size()-1).getTo();
						Position p = new Position(
								def.getX()+dir.x*d,
								def.getY()+dir.y*d);
						StepUnit stepUnit1 = new StepUnit(def, p);
						step.addStep(stepUnit1);
						if (new Validator().isValidStep(board, step, color)){
							try{
								board.apply(step);
								break outer;
							}catch(IllegalArgumentException e2){
								//board = copyOfBoard(origin);
								if (e2.getCause() instanceof DoOneMoreStepException){
									if (board.hasBecameQueen(color, p)){
										count = 7;
									}
									continue outer;
								}else{
									throw e2;
								}
							}
						}else{
							step.getSteps().remove(step.getSteps().size()-1);
						}
					}catch(IllegalArgumentException e2){
						step.getSteps().remove(step.getSteps().size()-1);
					}
				}
			}
			throw new IllegalArgumentException("No variants");
		}
	}
}
