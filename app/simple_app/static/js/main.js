// Connect to The Websocket (ExampleConsumer)
const myWebSocket = new WebSocket(`${document.body.dataset.scheme === 'http'? 'ws': 'wss'}://${document.body.dataset.host}/ws/spa-page/`);


/**
 * Send message to the backend
*/
function sendData(message, webSocket){
	webSocket.send(JSON.stringify(message));
}

/**
 * Send message to update page
 * @param {Event} event
 * @return {void}
*/
function handleClickNavigation(event) {
	event.preventDefault();
	sendData({
		action: 'change page',
		data: {
			page: event.target.dataset.target,
		}
	}, myWebSocket);
}
/**
 * Send new Lap
 * @param {Event} event
 * @return {void}
*/

function addLap(event){
	sendData({
		action: 'Add lap',
		data: {}
	}, myWebSocket);
} 

/**
 * Send new task to TODO list
 * @param {Event} event
 * @return {void}
*/
function addTask(event) {
	const task = document.querySelector('#task');
	sendData({
		action: 'Add task',
		data: {
			task: task.value
		}
	}, myWebSocket);
	// clear input
	task.value = '';
}

/**
 * Send message to WebSocket server to change the page
 * @param {WebSocket} webSocket
 * @return {void}
*/
function setEventsNavigation(webSocket) {
	// Navigation
	document.querySelectorAll(".nav__link--page").forEach(link =>{
		link.removeEventListener('click', handleClickNavigation, false);
		link.addEventListener('click', handleClickNavigation, false);
	});
}

// Event when a new message is received by WebSocket
myWebSocket.addEventListener("message", (event)=>{
	// Parse the data received
	const data = JSON.parse(event.data);
	// Renders the HTML received from the Consumer
	const selector = document.querySelector(data.selector);
	
	// If append is received, it will be appended.
	// Otherwise the entire DOM will be replaced.
	if (data.append){
		selector.innerHTML += data.html;
	} else {
		selector.innerHTML = data.html;
	}

	history.pushState({}, '', data.url);
	/**
	 * Reassigns the event of the newly rendered HTML
	*/
	updateEvents(); 
});

/**
 * Update events in every page
 * return {void}
*/
function updateEvents() {
	// Nav
	setEventsNavigation(myWebSocket);

	// Add lap
	const addLapButton = document.querySelector('#add-lap');
	if (addLapButton !== null) {
		addLapButton.removeEventListener('click', addLap, false);
		addLapButton.addEventListener('click', addLap, false);
	}

	// Add task
	const addTaskButton = document.querySelector('#add-task');
	if (addTaskButton !== null) {
		addTaskButton.removeEventListener('click', addTask, false);
		addTaskButton.addEventListener('click', addTask, false);
	}
} 

/*
		INITIALIZATION
*/
updateEvents();









