from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello():
	#return 'helloworld'
	if request.method == 'GET':
		return render_template('index.html')

@app.route('/user/<username>')
@app.route('/user/<username>/<int:post_id>', methods=['GET'])
def user(username, post_id=None):
	q = request.args.get('q', '') # /user/g?fields=name
	if post_id is not None:
		# request.form
		return '{}: {} with q={}'.format(
			username, post_id, q
		)
	return render_template(
		'user/index.html',
		username=username,
		q=q
	)


if __name__ == '__main__':
	app.run(debug=True)