document.addEventListener('DOMContentLoaded', ()=> {
    const togglePassword = document.querySelector('#eye-toggler');
    const password = document.querySelector('#id_password');
	// console.log(togglePassword);
	// console.log("togglePassword + password");
    
	togglePassword.onClick = toggle; 
	
	const toggle = (togglePassword, password) => {
		console.log("here");
		console.log(togglePassword);
		console.log(password);
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
		console.log(type);
		
        password.setAttribute('type', type);
        togglePassword.classList.toggle('fa-eye-slash');
    };
});