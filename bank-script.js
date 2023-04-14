const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get("id");
const apiUrl = "./bank.json";
const bannerFolder = "./assets/banner/";

fetch(apiUrl)
  .then((response) => response.json())
  .then((jsonData) => {
    console.log(jsonData);
    if (jsonData[userId]) {
      const userInfo = document.getElementById("user-info");

      const balance = jsonData[userId].balance;
      const lastUsed = new Date(jsonData[userId].last_used * 1000);
      const bannerList = jsonData[userId].banner;

      console.log(balance);
      console.log(lastUsed);
      console.log(bannerList);

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
          bannerNames += `<p>${bannerName}</p>`;
        }
      }

      console.log(bannerNames);

      // add the banner names to the user info container
      userInfo.innerHTML = `
        <p>BALANCE: <strong>${balance}</strong></p><br>
        <p>LAST USED:</p>
        <strong><p>${lastUsed.toLocaleString()}</p></strong><br>
        <p>CURRENT BANNER:</p>
        <strong><p>${jsonData[userId].currentbanner}</p></strong>
        <p>BANNER(S):</p>
        <strong>${bannerNames}</strong>
      `;
      if (currentBannerIndex >= 0) {
        const currentBannerName = bannerList[currentBannerIndex];
        const currentBannerDiv = document.createElement("p");
        currentBannerDiv.textContent = currentBannerName;
        userInfo.insertBefore(currentBannerDiv, userInfo.childNodes[5]);
      }
    }
  });
