(function () {
  const portfolio = {
    brand: {
      name: "Veronix",
      role: "Video Editing Studio",
      logo: "./logo.png"
    },
    seo: {
      homeTitle: "Veronix | Video Editing Portfolio",
      aboutTitle: "Veronix | About",
      description: "Veronix edits showreels, short form videos, and branded content for creators, businesses, and modern brands.",
      ogImage: "./assets/og-image.png"
    },
    social: {
      instagram: {
        label: "Instagram",
        url: "https://www.instagram.com/veronix.co/"
      },
      youtube: {
        label: "YouTube",
        url: "https://www.youtube.com/@veronix-co"
      },
      whatsapp: {
        label: "Book a call",
        url: "https://calendly.com/veronixx-media/30min"
      }
    },
    home: {
      overline: "Veronix - Video Editing Studio",
      desktopHeadline: "I edit videos &amp; enhance brand <span class=\"text-hero-serif\">visuals</span>",
      desktopNote: "Helped over 50+ clients! <br /><span class=\"text-hero-about-formerly\">Delivering top-notch videos for social media, commercials, and more.</span>",
      mobileHeadline: "I edit videos <span>&amp; enhance brand</span> <span class=\"text-hero-serif\">visuals</span>",
      mobileNote: "<span class=\"text-open-to-new-opportunities\">Helped over 50+ clients!<br /></span>Delivering top-notch videos for social media, commercials, and more.",
      selectedWorkLabel: "Selected Projects"
    },
    showreel: {
      eyebrow: "Showreel",
      title: "Director's Cut",
      description: "A fast paced montage built to show range, rhythm, premium pacing, and clean visual storytelling.",
      badge: "Watch on YouTube",
      link: "https://www.youtube.com/@veronix-co",
      target: "_blank"
    },

    shortformGallery: [
      { title: "Project 01", meta: "Short Form" },
      { title: "Project 02", meta: "Short Form" },
      { title: "Project 03", meta: "Short Form" },
      { title: "Project 04", meta: "Short Form" },
      { title: "Project 05", meta: "Short Form" },
      { title: "Project 06", meta: "Short Form" },
      { title: "Project 07", meta: "Short Form" },
      { title: "Project 08", meta: "Short Form" }
    ],
    contact: {
      eyebrow: "Contact",
      title: "Start the next edit.",
      text: "Project enquiries, short form work, and brand collaborations go through the contact link. Instagram and YouTube stay here for browsing work.",
      primaryLabel: "Book a call",
      note: "Fast replies for project enquiries."
    },
    about: {
      heading: "Veronix builds short form edits that feel polished, premium, and hard to skip.",
      bioHtml: "<span class=\"text-body-info-emphasis\">About Veronix</span><br /><br />Veronix is a video editing brand focused on short form content, visual polish, and sharp pacing for creators, brands, and businesses.<br /><br />The goal is simple: make every second feel intentional and every edit feel premium.<br />",
      experienceHtml: "<span class=\"text-body-info-emphasis\">What the work focuses on</span><br /><br />Retention driven hooks, clean captions, motion accents, color polish, and platform-ready delivery for reels, ads, and branded edits.<br /><br />If you need sharper visuals and better pacing, this site points people straight to the work and a direct contact link.<br />",
      imageA: "./assets/veronix-founder.png",
      imageB: "./assets/veronix-studio-work.png",
      signature: ""
    },
    footer: {
      copyright: "Copyright 2026 Veronix. All rights reserved.",
      note: "Instagram, YouTube, and Book a call available for enquiries.",
      updated: "Book a call"
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
        
        if (media.paused || media.ended) {
          safePlay(media);
          media.dataset.manualPlayback = "playing";
        } else {
          media.pause();
          media.dataset.manualPlayback = "paused";
        }
        updateToggleState(toggle, media);
      }

      toggle.addEventListener("click", togglePlayback);
      
      media.addEventListener("play", () => updateToggleState(toggle, media));
      media.addEventListener("pause", () => updateToggleState(toggle, media));

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

        // Prioritize native HLS on iOS/Safari for better stability in in-app browsers
        if ((isIOS || isSafari) && canPlayNative) {
          media.src = src;
        } else if (typeof Hls !== 'undefined' && Hls.isSupported()) {
          const hls = new Hls({
            startLevel: -1,
            capLevelToPlayerSize: true,
            enableWorker: true,
            autoStartLoad: true,
            manifestLoadingMaxRetry: 3,
            levelLoadingMaxRetry: 3
          });
          hls.loadSource(src);
          hls.attachMedia(media);
          
          hls.on(Hls.Events.MANIFEST_PARSED, function() {
            hls.currentLevel = hls.levels.length - 1;
          });

          // Recovery logic for stalls
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

  document.documentElement.lang = "en";
  bindText();
  bindHtml();
  bindAttribute("data-portfolio-content", "content");
  bindAttribute("data-portfolio-href", "href");
  bindAttribute("data-portfolio-src", "src");
  bindAttribute("data-portfolio-poster", "poster");
  bindTarget();
  bindBlankRel();
  bindHideIfEmpty();
  initVideos();
})();
