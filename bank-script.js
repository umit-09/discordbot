const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get("id");
const apiUrl = "https://84.211.187.101:8000";
const bannerFolder = "./assets/banner/";

fetch(apiUrl)
  .then((response) => response.json())
  .then((jsonData) => {
    console.log(response)
    if (jsonData[userId]) {
      const userInfo = document.getElementById("user-info");
      const balance = jsonData[userId].balance;
      const lastUsed = new Date(jsonData[userId].last_used * 1000);
      const bannerList = jsonData[userId].banner;

      // find the current banner and move it to the front of the list
      const currentBannerIndex = bannerList.indexOf(jsonData[userId].currentbanner);
      if (currentBannerIndex >= 0) {
        bannerList.splice(currentBannerIndex, 1);
        bannerList.unshift(jsonData[userId].currentbanner);
      }

      // create a div element for each banner name
      let bannerNames = "";
      for (let i = 0; i < bannerList.length; i++) {
        const bannerName = bannerList[i];
        if (bannerName !== "0") {
          bannerNames += `
            <div class="container">
              <img src="${bannerFolder}${bannerName}.png" alt="${bannerName}" draggable="false">
              <div class="centered">
                <h1>${bannerName}</h1>
              </div>
            </div>
          `;
        }
      }

      // add the banner names to the user info container
      userInfo.innerHTML = `
        <p>BALANCE: <strong>${balance}</strong></p><br>
        <p>LAST USED:</p>
        <strong><p>${lastUsed.toLocaleString()}</p></strong><br>
      `;

      if (jsonData[userId].currentbanner !== "0") {
        userInfo.innerHTML += `
          <p>CURRENT BANNER:</p>
          <div class="container">
            <img src="${bannerFolder}${jsonData[userId].currentbanner}.png" alt="${jsonData[userId].currentbanner}" draggable="false">
            <div class="centered">
              <h1>${jsonData[userId].currentbanner}</h1>
            </div>
          </div>
        `;
      }
      else {
        userInfo.innerHTML += `
          <p>CURRENT BANNER:</p>
          <p>This user is not using a banner</p><br>
        `;
      }

      userInfo.innerHTML += `
        <p>BANNER(S):</p>
        <strong>${bannerNames}</strong>
      `;
    } else {
      const userInfo = document.getElementById("user-info");
      userInfo.innerHTML = `
        <p>There is no one named <strong>${userId}</strong> registered</p>
      `;
    }
  });
if (/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) {
  document.getElementById("pc").style.display = "none";
  document.getElementById("mobile").style.display = "block";
}
else {
  document.getElementById("pc").style.display = "block";
  document.getElementById("mobile").style.display = "none";
}