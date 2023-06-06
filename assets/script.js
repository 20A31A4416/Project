// const URL = 'http://127.0.0.1:8000'
const URL = 'https://gg5.b62.mywebsitetransfer.com/medico'

const heroImages = [];
var scrollImages = '';
const portfolioDisplayImages = [];
var emotionalCaptureImages = '';

var emotionCount = 1;
var isHeroBackgroundSet = false;

var showMoreBtn = document.getElementById("showMoreBtn");
var imageContainer = document.getElementById("imageContainer");

var currentIndex = 0;
var batchSize = 6;

var scriptCount = 0;

// --------------------------------- Portfolio ----------------------------------------------
function showNextBatch() {
    var endIndex = currentIndex + batchSize;

    // Append the next batch of images to the imageContainer
    var html = "";
    for (var i = currentIndex; i < endIndex && i < portfolioDisplayImages.length; i++) {
        html += '<div class="col-12 col-lg-4 col-md-12 features-card">';
        html += '<img src="' + portfolioDisplayImages[i] + '" alt="">';
        html += '</div>';
    }
    imageContainer.innerHTML += html;

    currentIndex = endIndex;

    // Hide the "Show More" button if no more images are available
    if (currentIndex >= portfolioDisplayImages.length) {
        showMoreBtn.parentElement.style.display = "none";
    }
}

showMoreBtn.addEventListener("click", () => {showNextBatch()});


fetch(`${URL}/api/portfolio/`)
  .then(response => response.json())
  .then(data => {
    data.forEach(item => {
      if (item.isHeroBackground && !isHeroBackgroundSet) {
        document.querySelectorAll('.cid-t3PcmZ0dgn')[0].style.backgroundImage = `url(${item.link})`;
        isHeroBackgroundSet = true;
      }
      if (item.isHeroPic) {
        heroImages.push(item.link);
      }
      if (item.isScrollPic) {
        scrollImages += `<div class="embla__slide slider-image item" style="margin-left: 1rem; margin-right: 1rem;">
                            <div class="card-wrap">
                                <div class="item-wrapper position-relative">
                                    <div class="image-wrap">
                                        <img src="${item.link}" alt="">
                                    </div>
                                </div>
                            </div>
                        </div>`;
      }
      if (item.isPortfolioDisplay) {
        portfolioDisplayImages.push(item.link);
      }
      if (item.isEmotionalCapture && emotionCount < 4) {
        emotionalCaptureImages += `<div class="image-card"><img src="${item.link}" alt=""></div>`;
        emotionCount += 1;
      }
    });
    document.getElementById('scrollContainer').innerHTML = scrollImages;
    document.getElementById('emotionContainer').innerHTML = emotionalCaptureImages;
    showNextBatch(); // Show the initial batch of portfolio images

    //  Setting Hero Pics
    const heroPicList = document.getElementsByClassName('heroPic');
    heroPicList[0].src = heroImages[0]
    heroPicList[1].src = heroImages[1]
    heroPicList[2].src = heroImages[2]
    heroPicList[3].src = heroImages[3]
    heroPicList[4].src = heroImages[4]
    heroPicList[5].src = heroImages[5]

    scriptCount += 1;
  })
  .catch(error => {
    console.error('Error:', error);
  });


// --------------------------------- Plans ----------------------------------------------------

var planCount = 0;
var planElement = '';

fetch(`${URL}/api/plans/`)
  .then(response => response.json())
  .then(data => {
        data.forEach(plan => {
            planCount += 1;
            planElement += `<div class="col-md-4">
                    <div class="card pricing-box ${(planCount == 2) ? 'pricing-premium' : ''}">
                        <div class="card-block">
                            <h4 class="card-title">
                                ${plan.title}
                            </h4>
                            <h6 class="card-text">
                                <sup class="currency">
                                    ₹
                                </sup>
                                <span class="amount"">
                                    ${plan.price}
                                </span>
                            </h6>
                        </div>
                        <ul class="list-group list-group-flush">`
        
            var planAddons = plan.addons
            planAddons.forEach(addon => {
            planElement += `<li class="list-group-item text-center d-inline-block">${addon}</li>`
            });
          planElement += `
                      </ul>
                  </div>
              </div>`
    });
    document.getElementById('planList').innerHTML = planElement;
    scriptCount += 1;
  })
  .catch(error => {
    console.error('Error:', error);
  });


// --------------------------------- Feedbacks List----------------------------------------------------
  
  const handleSubmit = () => {
    const feedbackInput = document.getElementById('feedbackText');
    const feedbackByInput = document.getElementById('feedbackBy');
    const feedback = feedbackInput.value;
    const feedbackBy = feedbackByInput.value;
    
    // Create the payload object
    const payload = {
      reason: feedback,
      bookedBy: feedbackBy
    };
    
    // Send the POST request
    fetch(`${URL}/api/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
  })
  .then(response => {
    if (response.ok) {
      feedbackInput.value = "";
      feedbackByInput.value = "";
      window.alert('Appointment Request Sent Successfully..!');
    } else {
      window.alert('Expecting To Fill All Values...!')
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
};



// --------------------------------- Stream List ----------------------------------------------------

var streams = '';
var streamCount = 0;

fetch(`${URL}/api/streams/`)
.then(response => response.json())
.then(data => {
  data = data.slice(0,4);
  data.forEach(streamData => {
    streamCount += 1;
    streams += `<div class="col-12 col-lg-3 col-md-6 card item features-image">
                    <div class="item-wrapper">
                        <img src="${streamData.link}" alt="">
                        <a href="${streamData.streamLink}" target="_blank" class="card-link">
                            <div class="card-wrapper">
                                <p class="mbr-number mbr-fonts-style display-5">
                                    <strong>${streamCount}</strong>
                                </p>
                                <div class="card-text">
                                    <h4 class="mbr-title mbr-fonts-style display-5">
                                        <strong>${streamData.title}</strong>
                                    </h4>
                                    <p class="mbr-text mbr-fonts-style display-7">
                                        ${streamData.date}, ${streamData.time}
                                    </p>
                                    <span class="mbr-iconfont mobi-mbri-right mobi-mbri"></span>
                                </div>
                            </div>
                        </a>
                    </div>
                </div>`
        });
      document.getElementById('streamContainer').innerHTML = streams;
      scriptCount += 1;
    })
    .catch(error => {
      console.error('Error:', error);
    });


//-------------------------------------- categories -------------------------------------------

var categories = '';

fetch(`${URL}/api/categories/`)
.then(response => response.json())
.then(data => {
  data = data.slice(0,4);
  data.forEach(category => {
    categories += `<div class="col-12 col-lg-4 card">
                    <div class="card-wrapper">
                        <img src="${category.link}" alt="">
                        <h4 class="mbr-card-title mbr-fonts-style display-5">
                            ${category.title}</h4>
                        <p class="mbr-card-desc mbr-fonts-style display-7">
                            ${category.description}</p>
                    </div>
                </div>`
        });
      document.getElementById('categoryContainer').innerHTML = categories;
      scriptCount += 1;
    })
    .catch(error => {
      console.error('Error:', error);
    });



// ----------------------- scroll to the position

window.addEventListener('load', function () {
  var hash = window.location.hash;
  if (hash) {
    var targetElement = document.getElementById(hash.substring(1));
    if (targetElement) {
      setTimeout(function() {
        targetElement.scrollIntoView();
      }, 0);
    }
  }
  var checkScriptStatus = setInterval(() => {
    if (scriptCount == 5) {    
      // Create the script element
      const script = document.createElement('script');
      script.src = 'assets/embla/embla.min.js';
      script.type = 'text/javascript';
      script.onload = () => {
        const Nscript = document.createElement('script');
        Nscript.src = 'assets/embla/script.js ';
        Nscript.type = 'text/javascript';
        document.body.appendChild(Nscript);
      }
      document.body.appendChild(script);
      clearInterval(checkScriptStatus);
    }
  }, 100);
});



  
