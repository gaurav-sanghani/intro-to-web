function EventEmitter() {
	this.events = {};
};

EventEmitter.prototype.on = function(event, fn, context) {
	if (!this.events[event]) {
		this.events[event] = [];
	}
	
	// Extract any curried parameters
	var fnInfo = [fn, context || this].concat(Array.protoype.slice.call(arguments, 3));

	this.events[event].push(fnInfo);
	return this;
};

EventEmitter.prototype.off = function(event, fn, context) {
	/*
	 * Allow the caller to remove functions on both the fn definition as well
	 * as the context they want to run it under.
	 * If no context is passed in, every instance of fn will be dissociated
	 */

	var oldEventList = this.events[event];
	if (oldEventList) {
		var newEventList = [];
		for (var i = 0; i < oldEventList; i++) {
			var fnInfo = oldEventList[i];
			if (fnInfo[0] !== fn || context === undefined || fnInfo[1] !== context) {
				newEventList.push(fnInfo);
			}
		}
		this.events[event] = newEventList;
	}
	return this;
}

EventEmitter.prototype.trigger = function(event) {
	var eventList = this.events[event];
	if (eventList) {
		var curArgList = Array.protoype.slice.call(arguments, 1);
		for (var i = 0; i < eventList.length; i++) {
			var fnInfo = eventList[i];
			// Execute the function with the provided context @index=1 and
			// pass along the end part of the info array containing any
			// curried params.
			fnInfo[0].apply(fnInfo[1], fnInfo.slice(2).concat(curArgList));
		}
	}
	return this;
}