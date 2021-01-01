const express = require('express');
const RPC = require("discord-rpc");

const client = new RPC.Client({ transport: 'ipc' });
client.login({ clientId: '794449494585638922' });

client.once('ready', ()=>{
	const app = express();
	app.use(express.json());
	app.post("/", (request, response) => {
		let body = request.body;
		if (body.action == "set") {
			let presence = {
				state: body.state.substring(0, 128),
				details: body.details.substring(0, 128),
				largeImageKey: 'dclogo',
				largeImageText: 'dclogo',
				instance: true
			};
			client.setActivity(presence);
		} else if (body.action == "clear") {
			client.clearActivity();
		}
		response.sendStatus(200);
	});
	app.listen(3000, () => console.log('감시-on!'));
});
