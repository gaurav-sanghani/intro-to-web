ITEM_ENDPOINT = '/items'
function ItemModel(data, created_ts) {
	this.data = data;
	this.created_ts = created_ts || new Date();
};

ItemModel.prototype = new EventEmitter();


ItemModel.prototype.save = function() {
	req = new XMLHttpRequest();
	req.open('POST', ITEM_ENDPOINT);
};


ITEMVIEW_DEFAULT_EL = 'li';
function ItemView(el, model) {
	this.el = el || document.createElement(ITEMVIEW_DEFAULT_EL);
	this.model = model;
}

ItemView.prototype.render = function() {
	this.el.textContent = this.model.data;
	return this;
};



function TodoModel() {
	this.items = [];
};

TodoModel.prototype = new EventEmitter();

TodoModel.prototype.addItem = function(data) {
	var item = new ItemModel(data);
	// item.save();
	this.items.push(item);
	this.trigger('add', item);
};


function TodoView(el) {
	var self = this;

	this.el = el;
	this.el.getElementsByTagName('button')[0].onclick(function() {
		
	});

	this.model = (
		new TodoModel()
	).on(
		'add',
		this.addItem,
		this
	);
};

TodoView.prototype.addItem = function(item) {
	this.el.getElementsByTagName('ul')[0].appendChild(
		(new ItemView(null, item)).render().el
	);
	return this;
};

TodoView.prototype.toggleTextArea = function() {
	var textarea = self.el.getElementsByTagName('textarea')[0];
	if (textarea.classList.contains('hidden')) {
		textarea.classList.remove('hidden');
	} else {
		textarea.classList.add('hidden');
	}
}

