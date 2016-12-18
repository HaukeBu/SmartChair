package com.hawhamburg.sg.data;

import org.influxdb.dto.Point.Builder;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public abstract class AbstractValue {
	
	private double value;
	
	public AbstractValue( double value){
		this.value = value;
	}
	
	public double getValue() {
		return value;
	}
	
	public abstract void addValueToPoint(Builder pointBuilder);
	
}
