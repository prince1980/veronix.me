(function () {
  const portfolio = {
    brand: {
      name: "Veronix Co",
      role: "Video Editing Studio",
      logo: "./logo.png"
    },
    seo: {
      homeTitle: "Veronix Co | Premium Short Form Video Editing Studio",
      aboutTitle: "About Veronix Co | Video Editing Agency in Ahmedabad",
      description: "Veronix Co is a premium short form video editing studio in Ahmedabad, specializing in retention-driven reels, ads, creator content, and visual storytelling.",
      ogImage: "./assets/og-image.png"
    },
    social: {
      instagram: {
        label: "Instagram",
        url: "https://www.instagram.com/veronix.co/"
      },
      linkedin: {
        label: "LinkedIn",
        url: "https://www.linkedin.com/in/veronix-co-919a93371/"
      },
      whatsapp: {
        label: "Book a call",
        url: "https://cal.com/veronix/30min"
      }
    },
    home: {
      overline: "Veronix Co - Premium Video Editing Studio",
      desktopHeadline: "Premium short form video editing &amp; <span class=\"text-hero-serif\">brand visuals</span>",
      desktopNote: "Veronix is a creative editing studio in Ahmedabad.<br /><span class=\"text-hero-about-formerly\">Specializing in retention-driven reels, social media ads, and creator content.</span>",
      mobileHeadline: "Premium short form video editing <span>&amp;</span> <span class=\"text-hero-serif\">brand visuals</span>",
      mobileNote: "<span class=\"text-open-to-new-opportunities\">Veronix is a creative studio based in Ahmedabad.<br /></span>Specializing in retention-driven reels, ads, and creator content.",
      selectedWorkLabel: "Selected Projects"
    },
    showreel: {
      eyebrow: "Showreel",
      title: "Director's Cut",
      description: "A fast paced montage built to show range, rhythm, premium pacing, and clean visual storytelling.",
      badge: "Watch on LinkedIn",
      link: "https://www.linkedin.com/in/veronix-co-919a93371/",
      target: "_blank"
    },

    shortformGallery: [
      { title: "Project 01", meta: "Talking Head Videos" },
      { title: "Project 02", meta: "Talking Head Videos" },
      { title: "Project 03", meta: "Talking Head Videos" },
      { title: "Project 04", meta: "Meta Ad Creatives" },
      { title: "Project 05", meta: "Meta Ad Creatives" },
      { title: "Project 06", meta: "Meta Ad Creatives" }
    ],
    contact: {
      eyebrow: "Contact",
      title: "Start the next edit.",
      text: "Project enquiries, short form work, and brand collaborations go through the contact link. Instagram and LinkedIn stay here for browsing work.",
      primaryLabel: "Book a call",
      note: "Fast replies for project enquiries."
    },
    about: {
      heading: "Veronix Co builds short form edits that feel polished, premium, and retention-driven.",
      bioHtml: "<span class=\"text-body-info-emphasis\">About Veronix Co</span><br /><br />Veronix Co is a premium video editing studio based in Ahmedabad, Gujarat, India, focused on short form content, visual storytelling, and sharp pacing for creators, brands, and businesses.<br /><br />We specialize in retention-focused editing, ensuring every second feels intentional and every reel, ad, or TikTok feels premium.<br />",
      experienceHtml: "<span class=\"text-body-info-emphasis\">Our Editing Expertise</span><br /><br />Retention-driven hooks, clean captions, motion graphics, color polish, and platform-ready delivery for Instagram reels, YouTube shorts, social media ads, and branded short form edits.<br /><br />If you need sharper visual aesthetics and premium video editing, explore our work or book a consultation.<br />",
      imageA: "./assets/veronix-founder.png",
      imageB: "./assets/veronix-studio-work.png",
      signature: ""
    },
    footer: {
      copyright: "Copyright 2026 Veronix Co. All rights reserved.",
      note: "Instagram and LinkedIn available for enquiries.",
      updated: ""
    }
  };

  function getValue(path) {
    return path.split(".").reduce(function (value, key) {
      if (value == null) {
        return undefined;
      }

      if (/^\d+$/.test(key)) {
        return value[Number(key)];
      }

      return value[key];
    }, portfolio);
  }

  function bindText() {
    document.querySelectorAll("[data-portfolio-text]").forEach(function (element) {
      const value = getValue(element.getAttribute("data-portfolio-text"));

      if (value != null) {
        element.textContent = value;
      }
    });
  }

  function bindHtml() {
    document.querySelectorAll("[data-portfolio-html]").forEach(function (element) {
      const value = getValue(element.getAttribute("data-portfolio-html"));

      if (value != null) {
        element.innerHTML = value;
      }
    });
  }

  function bindAttribute(dataAttribute, attribute) {
    document.querySelectorAll("[" + dataAttribute + "]").forEach(function (element) {
      const value = getValue(element.getAttribute(dataAttribute));

      if (value == null || value === "") {
        element.removeAttribute(attribute);
        return;
      }

      element.setAttribute(attribute, value);

      if (attribute === "src" && element.tagName === "IMG") {
        element.removeAttribute("srcset");
      }

      if (attribute === "src" && element.tagName === "VIDEO") {
        element.load();
      }
    });
  }

  function bindTarget() {
    document.querySelectorAll("[data-portfolio-target]").forEach(function (element) {
      const value = getValue(element.getAttribute("data-portfolio-target"));

      if (value) {
        element.setAttribute("target", value);
        element.setAttribute("rel", "noopener noreferrer");
      } else {
        element.removeAttribute("target");
        element.removeAttribute("rel");
      }
    });
  }

  function bindBlankRel() {
    document.querySelectorAll('a[target="_blank"]').forEach(function (element) {
      element.setAttribute("rel", "noopener noreferrer");
    });
  }

  function bindHideIfEmpty() {
    document.querySelectorAll("[data-portfolio-hide-if-empty]").forEach(function (element) {
      const value = getValue(element.getAttribute("data-portfolio-hide-if-empty"));

      if (!value) {
        element.style.display = "none";
      }
    });
  }

  function initVideos() {
    const supportsHover = window.matchMedia("(hover: hover)").matches;

    function safePlay(media) {
      if (media.play && typeof media.play === "function") {
        const playPromise = media.play();
        if (playPromise && typeof playPromise.catch === "function") {
          playPromise.catch(function () {});
        }
      }
    }

    function updateToggleState(toggle, media) {
      if (!toggle) return;
      const isPlaying = !media.paused && !media.ended;
      toggle.classList.toggle("is-playing", isPlaying);
      toggle.setAttribute("aria-label", isPlaying ? "Pause video" : "Play video");
    }

    function attachToggle(media) {
      const frame = media.closest(".veronix-showreel-frame") ||
                    media.closest(".veronix-feature-poster") ||
                    media.closest(".veronix-reel-thumb");

      if (!frame) return null;
      const toggle = frame.querySelector(".veronix-play-pill");
      if (!toggle) return null;

      function togglePlayback(event) {
        event.preventDefault();
        event.stopPropagation();
        
        const volumeToggle = frame.querySelector(".veronix-volume-pill");

        if (media.paused || media.ended) {
          media.muted = false; // Unmute on play
          safePlay(media);
          media.dataset.manualPlayback = "playing";
        } else {
          media.pause();
          media.muted = true; // Mute on pause
          media.dataset.manualPlayback = "paused";
        }
        
        if (volumeToggle) {
          volumeToggle.classList.toggle("is-unmuted", !media.muted);
          volumeToggle.setAttribute("aria-label", media.muted ? "Unmute video" : "Mute video");
        }
        
        updateToggleState(toggle, media);
      }

      toggle.addEventListener("click", togglePlayback);
      
      media.addEventListener("play", function() {
        updateToggleState(toggle, media);
        const volumeToggle = frame.querySelector(".veronix-volume-pill");
        if (volumeToggle) {
          volumeToggle.classList.toggle("is-unmuted", !media.muted);
        }
      });
      media.addEventListener("pause", function() {
        updateToggleState(toggle, media);
        const volumeToggle = frame.querySelector(".veronix-volume-pill");
        if (volumeToggle) {
          volumeToggle.classList.toggle("is-unmuted", !media.muted);
        }
      });

      updateToggleState(toggle, media);
      return toggle;
    }

    function attachVolumeToggle(media) {
      const frame = media.closest(".veronix-showreel-frame") ||
                    media.closest(".veronix-feature-poster") ||
                    media.closest(".veronix-reel-thumb");

      if (!frame) return null;
      const volumeToggle = frame.querySelector(".veronix-volume-pill");
      if (!volumeToggle) return null;

      function updateVolumeState() {
        volumeToggle.classList.toggle("is-unmuted", !media.muted);
        volumeToggle.setAttribute("aria-label", media.muted ? "Unmute video" : "Mute video");
      }

      volumeToggle.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        media.muted = !media.muted;
        updateVolumeState();
      });

      updateVolumeState();
      return volumeToggle;
    }

    function formatTime(seconds) {
      const min = Math.floor(seconds / 60);
      const sec = Math.floor(seconds % 60);
      return (min < 10 ? "0" + min : min) + ":" + (sec < 10 ? "0" + sec : sec);
    }

    document.querySelectorAll("video.veronix-reel-media, video[data-portfolio-video]").forEach(function (media) {
      const src = media.getAttribute("data-portfolio-src") || media.getAttribute("src");
      const chip = media.closest(".veronix-reel-thumb") ? media.closest(".veronix-reel-thumb").querySelector(".veronix-duration-chip") : null;

      if (src && src.includes(".m3u8")) {
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
        const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
        const canPlayNative = media.canPlayType('application/vnd.apple.mpegurl');

        // Fidelity-First Configuration: Try Hls.js even on iOS for quality control
        if (typeof Hls !== 'undefined' && Hls.isSupported()) {
          const hls = new Hls({
            startLevel: 99, // Force highest start level
            capLevelToPlayerSize: false,
            enableWorker: true,
            autoStartLoad: true,
            maxBufferLength: 60,
            maxMaxBufferLength: 120,
            manifestLoadingMaxRetry: 20,
            levelLoadingMaxRetry: 20,
            fragLoadingMaxRetry: 20,
            initialLiveManifestSize: 1,
            enableLowLatencyMode: true
          });
          hls.loadSource(src);
          hls.attachMedia(media);
          
          // Thumbnail stabilizer: Mirror poster to background to prevent "fading" during engine init
          if (media.getAttribute("poster")) {
            media.style.backgroundImage = `url(${media.getAttribute("poster")})`;
            media.style.backgroundSize = "cover";
            media.style.backgroundPosition = "center";
          }

          hls.on(Hls.Events.MANIFEST_PARSED, function() {
            // Filter out low-res levels and force 1080p, 2k, 4k only
            let highestIndex = hls.levels.length - 1;
            
            // Lock to the absolute highest available quality
            hls.currentLevel = highestIndex;
            hls.autoLevelEnabled = false; 
            hls.startLevel = highestIndex;
          });



          hls.on(Hls.Events.ERROR, function (event, data) {
            if (data.fatal) {
              switch (data.type) {
                case Hls.ErrorTypes.NETWORK_ERROR:
                  hls.startLoad();
                  break;
                case Hls.ErrorTypes.MEDIA_ERROR:
                  hls.recoverMediaError();
                  break;
                default:
                  hls.destroy();
                  if (canPlayNative) media.src = src;
                  break;
              }
            }
          });

          hls.on(Hls.Events.SUBTITLE_TRACKS_UPDATED, function() {
            hls.subtitleTrack = -1;
            hls.subtitleDisplay = false;
          });
        } else if (canPlayNative) {
          media.src = src;
        }
      } else if (src) {
        media.src = src;
      }

      media.muted = true;
      media.autoplay = false;
      media.dataset.manualPlayback = "paused";
      
      media.addEventListener("loadedmetadata", function() {
        if (chip && media.duration && media.duration !== Infinity) {
          chip.textContent = formatTime(media.duration);
        }
      });

      media.addEventListener("play", function (event) {
        if (media.dataset.manualPlayback !== "playing") {
          media.pause();
        }
      });

      attachToggle(media);
      attachVolumeToggle(media);
    });
  }

  function initFaq() {
    document.querySelectorAll(".veronix-faq-item").forEach(function (item) {
      const button = item.querySelector(".veronix-faq-question");
      const answer = item.querySelector(".veronix-faq-answer");

      if (!button || !answer) return;

      function setOpen(isOpen) {
        item.classList.toggle("is-open", isOpen);
        button.setAttribute("aria-expanded", isOpen ? "true" : "false");

        if (isOpen) {
          answer.hidden = false;
          answer.style.maxHeight = answer.scrollHeight + "px";
        } else {
          answer.style.maxHeight = answer.scrollHeight + "px";
          requestAnimationFrame(function () {
            answer.style.maxHeight = "0px";
          });
          window.setTimeout(function () {
            if (!item.classList.contains("is-open")) {
              answer.hidden = true;
            }
          }, 320);
        }

        window.setTimeout(function () {
          window.dispatchEvent(new Event("resize"));
        }, 340);
      }

      button.addEventListener("click", function () {
        setOpen(button.getAttribute("aria-expanded") !== "true");
      });
    });
  }

  function cleanUrls() {
    try {
      let path = window.location.pathname;
      if (path.endsWith("/index.html")) {
        window.history.replaceState({}, document.title, path.replace("/index.html", "/"));
      } else if (path.endsWith(".html")) {
        window.history.replaceState({}, document.title, path.replace(".html", ""));
      }
    } catch (e) {}
  }

  document.documentElement.lang = "en";
  cleanUrls();
  bindText();
  bindHtml();
  bindAttribute("data-portfolio-content", "content");
  bindAttribute("data-portfolio-href", "href");
  bindAttribute("data-portfolio-poster", "poster");
  // Removed direct src binding to prevent clashing with HLS initialization logic
  // bindAttribute("data-portfolio-src", "src"); 
  bindTarget();
  bindBlankRel();
  bindHideIfEmpty();
  initVideos();
  initFaq();
  // Mobile / In-App Browser Navbar Fix
  document.addEventListener('DOMContentLoaded', function() {
    const isMobile = window.innerWidth <= 991;
    const isInAppBrowser = /Instagram|FBAN|FBAV|Line|Snapchat|LinkedIn/i.test(navigator.userAgent);
    const navSection = document.querySelector('.section-nav');
    
    if (navSection && isMobile) {
      if (isInAppBrowser) {
        document.documentElement.classList.add('is-inapp-browser');
      }
      
      window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
          navSection.classList.add('nav-scrolled');
        } else {
          navSection.classList.remove('nav-scrolled');
        }
      }, { passive: true });
    }
  });
})();
