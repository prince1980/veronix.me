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
      ogImage: "./logo.png"
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
        label: "Contact Us",
        url: "https://wa.me/8780764063"
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
      target: "_blank",
      panels: [
        {
          label: "Long Form 01",
          meta: "16:9 Edit",
          poster: "./assets/showreel-v1.jpg",
          video: "./v1.mp4",
          duration: "00:25"
        },
        {
          label: "Long Form 02",
          meta: "16:9 Edit",
          poster: "./assets/showreel-v2.jpg",
          video: "./v2.mp4",
          duration: "00:14"
        }
      ]
    },
    shortformFeature: {
      eyebrow: "Short Form",
      title: "Short Form Edits",
      description: "<span class=\"text-projectcard-description-company\">Instagram Reels, 2026</span> - Fast edits made for reach, retention, and clean pacing.",
      badge: "Featured Reel",
      link: "https://www.instagram.com/veronix.co/",
      target: "_blank",
      previewPoster: "./assets/short-01.jpg",
      previewVideo: "./1.mp4",
      duration: "00:31",
      detailTitle: "Retention Led Cuts",
      detailText: "Hook first pacing, sharp subtitle treatment, motion accents, and polished finishing built for vertical screens."
    },
    shortformGallery: [
      {
        title: "Short Form 01",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-01.jpg",
        video: "./1.mp4",
        duration: "00:31"
      },
      {
        title: "Short Form 02",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-02.jpg",
        video: "./2.mp4",
        duration: "00:29"
      },
      {
        title: "Short Form 03",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-03.jpg",
        video: "./3.mp4",
        duration: "00:39"
      },
      {
        title: "Short Form 04",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-04.jpg",
        video: "./4.mp4",
        duration: "00:47"
      },
      {
        title: "Short Form 05",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-05.jpg",
        video: "./5.mp4",
        duration: "00:31"
      },
      {
        title: "Short Form 06",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-06.jpg",
        video: "./6.mp4",
        duration: "00:44"
      },
      {
        title: "Short Form 07",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-07.jpg",
        video: "./7.mp4",
        duration: "00:45"
      },
      {
        title: "Short Form 08",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-08.jpg",
        video: "./8.mp4",
        duration: "01:14"
      },
      {
        title: "Short Form 09",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-09.jpg",
        video: "./9.mp4",
        duration: "00:53"
      },
      {
        title: "Short Form 10",
        meta: "Vertical Reel",
        link: "https://www.instagram.com/veronix.co/",
        target: "_blank",
        poster: "./assets/short-10.jpg",
        video: "./10.mp4",
        duration: "01:37"
      }
    ],
    contact: {
      eyebrow: "Contact",
      title: "Start the next edit.",
      text: "Project enquiries, short form work, and brand collaborations go through the contact link. Instagram and YouTube stay here for browsing work.",
      primaryLabel: "Contact Us",
      note: "Fast replies for project enquiries."
    },
    about: {
      heading: "Veronix builds short form edits that feel polished, premium, and hard to skip.",
      bioHtml: "<span class=\"text-body-info-emphasis\">About Veronix</span><br /><br />Veronix is a video editing brand focused on short form content, visual polish, and sharp pacing for creators, brands, and businesses.<br /><br />The goal is simple: make every second feel intentional and every edit feel premium.<br />",
      experienceHtml: "<span class=\"text-body-info-emphasis\">What the work focuses on</span><br /><br />Retention driven hooks, clean captions, motion accents, color polish, and platform-ready delivery for reels, ads, and branded edits.<br /><br />If you need sharper visuals and better pacing, this site points people straight to the work and a direct contact link.<br />",
      imageA: "./assets/about-01.svg",
      imageB: "./assets/about-02.svg",
      signature: ""
    },
    footer: {
      copyright: "Copyright 2026 Veronix. All rights reserved.",
      note: "Instagram, YouTube, and Contact Us available for enquiries.",
      updated: "Contact Us"
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
      const playPromise = media.play();

      if (playPromise && typeof playPromise.catch === "function") {
        playPromise.catch(function () {});
      }
    }

    function updateToggleState(toggle, media) {
      if (!toggle) {
        return;
      }

      const isPlaying = !media.paused && !media.ended;
      toggle.classList.toggle("is-playing", isPlaying);
      toggle.setAttribute("aria-label", isPlaying ? "Pause video" : "Play video");
    }

    function attachToggle(media) {
      const frame =
        media.closest(".veronix-showreel-frame") ||
        media.closest(".veronix-feature-poster") ||
        media.closest(".veronix-reel-thumb");

      if (!frame) {
        return null;
      }

      const toggle = frame.querySelector(".veronix-play-pill");

      if (!toggle) {
        return null;
      }

      toggle.setAttribute("role", "button");
      toggle.setAttribute("tabindex", "0");
      toggle.setAttribute("aria-label", "Play video");
      toggle.setAttribute("aria-pressed", "false");

      function togglePlayback(event) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();

        if (media.paused || media.ended) {
          safePlay(media);
          media.dataset.manualPlayback = "playing";
        } else {
          media.pause();
          media.dataset.manualPlayback = "paused";
        }

        updateToggleState(toggle, media);
        toggle.setAttribute("aria-pressed", String(!media.paused && !media.ended));
      }

      toggle.addEventListener("click", togglePlayback);
      toggle.addEventListener("keydown", function (event) {
        if (event.key !== "Enter" && event.key !== " ") {
          return;
        }

        togglePlayback(event);
      });

      media.addEventListener("play", function () {
        updateToggleState(toggle, media);
        toggle.setAttribute("aria-pressed", "true");
      });

      media.addEventListener("pause", function () {
        updateToggleState(toggle, media);
        toggle.setAttribute("aria-pressed", "false");
      });

      updateToggleState(toggle, media);
      return toggle;
    }

    function attachVolumeToggle(media) {
      const frame =
        media.closest(".veronix-showreel-frame") ||
        media.closest(".veronix-feature-poster") ||
        media.closest(".veronix-reel-thumb");

      if (!frame) {
        return null;
      }

      const volumeToggle = frame.querySelector(".veronix-volume-pill");

      if (!volumeToggle) {
        return null;
      }

      function updateVolumeState() {
        volumeToggle.classList.toggle("is-unmuted", !media.muted);
        volumeToggle.setAttribute("aria-label", media.muted ? "Unmute video" : "Mute video");
      }

      function toggleVolume(event) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();

        // When unmuting one, unmute all to provide a better "sound on" experience
        const shouldMute = !media.muted;
        document.querySelectorAll("video").forEach((v) => {
          v.muted = shouldMute;
        });

        // Update all toggle UI states
        document.querySelectorAll(".veronix-volume-pill").forEach((pill) => {
          pill.classList.toggle("is-unmuted", !shouldMute);
        });
      }

      volumeToggle.addEventListener("click", toggleVolume);
      updateVolumeState();
      return volumeToggle;
    }

    document.querySelectorAll("video[data-portfolio-video]").forEach(function (media) {
      const source = media.getAttribute("src");

      if (!source) {
        return;
      }

      media.muted = true;
      media.autoplay = false;
      media.loop = true;
      media.playsInline = true;
      media.preload = "metadata";

      // Prevent scripts from auto-playing videos unless marked as manual playback
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
