$(document).ready(function(){
    let inactivityTime = 180000;
    let time;

    function logout(){
        // Redirect the user to logout or login page
        window.location.href = "login/"
    }

    function resetTmer(){
        clearTimeout(time);
        time = setTimeout(logout, inactivityTime);
    }

    $(document).on('mousemove keypress', function(){
        resetTmer();
    });

    resetTmer();
});

