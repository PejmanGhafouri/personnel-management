
// ------- Sign Up -------- //

// ------- CountDown -------- //
function countdown(duration) {

  let time = duration * 60;
  const countdown = document.getElementById("countdown");
  document.getElementById("resend").disabled = true;
  countdown.innerHTML = "(--:--)"
  let countInterval = setInterval(function () {
    let minuets = Math.floor(time / 60);
    let seconds = time % 60;

    if (seconds < 10) seconds = `0${seconds}`;
    if (minuets < 10) minuets = `0${minuets}`;

    if (Number(seconds) === 0 && Number(minuets) === 0) {
      document.getElementById("resend").disabled = false;
      countdown.innerHTML = `(${minuets} : ${seconds})`;
      clearInterval(countInterval);
    }
    else {
      countdown.innerHTML = `(${seconds} : ${minuets})`;
      time--;
    }

  }, 1000)
}

d.addEventListener("DOMContentLoaded", function (event) {
  let countdownDuration = 2;

  countdown(countdownDuration)

  document.getElementById("resend").onclick = function () {
    countdown(countdownDuration)
  }
});
