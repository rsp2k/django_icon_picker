class IconPicker {
  constructor(options) {
    this.searchInput = document.getElementById(options.searchInputId);
    this.selectedIcon = document.getElementById("selectedIcon");
    this.resultsDiv = document.getElementById("results");
    this.colorPicker = document.getElementById("color");
    this.savePath = options.savePath;
    this.selectedPrefix = "";
    this.form = document.getElementById(`${options.model}_form`);
    this.objectId = options.objectId;
    this.model = options.model;
    this.icon = "";
    this.currentMode = "icons"; // "icons" or "emojis"

    // Initialize emoji data
    this.initializeEmojiData();
    this.init();
  }

  init() {
    this.setupInitialIcon();
    this.setupEventListeners();
    this.createModeToggle();
  }

  initializeEmojiData() {
    // Curated emoji dataset with categories and keywords for better search
    this.emojiData = [
      // Smileys & People
      { emoji: "😀", name: "grinning face", keywords: ["happy", "smile", "grin", "joy"], category: "smileys" },
      { emoji: "😃", name: "grinning face with big eyes", keywords: ["happy", "smile", "joy", "cheerful"], category: "smileys" },
      { emoji: "😄", name: "grinning face with smiling eyes", keywords: ["happy", "smile", "joy", "laugh"], category: "smileys" },
      { emoji: "😁", name: "beaming face with smiling eyes", keywords: ["happy", "smile", "grin", "joy"], category: "smileys" },
      { emoji: "😊", name: "smiling face with smiling eyes", keywords: ["happy", "smile", "blush", "pleasant"], category: "smileys" },
      { emoji: "😍", name: "smiling face with heart-eyes", keywords: ["love", "heart", "adore", "crush"], category: "smileys" },
      { emoji: "🤔", name: "thinking face", keywords: ["think", "consider", "hmm", "ponder"], category: "smileys" },
      { emoji: "😎", name: "smiling face with sunglasses", keywords: ["cool", "awesome", "sunglasses", "confident"], category: "smileys" },
      { emoji: "🙄", name: "face with rolling eyes", keywords: ["eye roll", "annoyed", "whatever"], category: "smileys" },
      { emoji: "😴", name: "sleeping face", keywords: ["sleep", "tired", "zzz", "rest"], category: "smileys" },
      { emoji: "🤯", name: "exploding head", keywords: ["mind blown", "shocked", "amazed"], category: "smileys" },
      { emoji: "🥳", name: "partying face", keywords: ["party", "celebrate", "birthday", "fun"], category: "smileys" },
      
      // Hand gestures
      { emoji: "👍", name: "thumbs up", keywords: ["like", "approve", "good", "yes", "ok"], category: "people" },
      { emoji: "👎", name: "thumbs down", keywords: ["dislike", "bad", "no", "disapprove"], category: "people" },
      { emoji: "👋", name: "waving hand", keywords: ["wave", "hello", "hi", "goodbye", "bye"], category: "people" },
      { emoji: "👏", name: "clapping hands", keywords: ["clap", "applause", "bravo", "congratulations"], category: "people" },
      { emoji: "🙏", name: "folded hands", keywords: ["pray", "thanks", "please", "namaste"], category: "people" },
      { emoji: "✋", name: "raised hand", keywords: ["stop", "high five", "hand", "halt"], category: "people" },
      { emoji: "🤝", name: "handshake", keywords: ["handshake", "deal", "agreement", "partnership"], category: "people" },
      { emoji: "💪", name: "flexed biceps", keywords: ["strong", "muscle", "strength", "power"], category: "people" },
      
      // Hearts & Love
      { emoji: "❤️", name: "red heart", keywords: ["love", "heart", "red", "romance"], category: "symbols" },
      { emoji: "💙", name: "blue heart", keywords: ["love", "heart", "blue", "trust"], category: "symbols" },
      { emoji: "💚", name: "green heart", keywords: ["love", "heart", "green", "nature"], category: "symbols" },
      { emoji: "💛", name: "yellow heart", keywords: ["love", "heart", "yellow", "friendship"], category: "symbols" },
      { emoji: "🧡", name: "orange heart", keywords: ["love", "heart", "orange", "warmth"], category: "symbols" },
      { emoji: "💜", name: "purple heart", keywords: ["love", "heart", "purple", "compassion"], category: "symbols" },
      { emoji: "🖤", name: "black heart", keywords: ["love", "heart", "black", "dark"], category: "symbols" },
      { emoji: "🤍", name: "white heart", keywords: ["love", "heart", "white", "pure"], category: "symbols" },
      { emoji: "💕", name: "two hearts", keywords: ["love", "hearts", "romance", "couple"], category: "symbols" },
      
      // Activities & Objects
      { emoji: "🎉", name: "party popper", keywords: ["party", "celebration", "confetti", "celebrate"], category: "activities" },
      { emoji: "🎊", name: "confetti ball", keywords: ["party", "celebration", "confetti", "festive"], category: "activities" },
      { emoji: "🎁", name: "wrapped gift", keywords: ["gift", "present", "birthday", "surprise"], category: "activities" },
      { emoji: "🎂", name: "birthday cake", keywords: ["cake", "birthday", "celebration", "dessert"], category: "food" },
      { emoji: "🏆", name: "trophy", keywords: ["trophy", "award", "winner", "champion", "prize"], category: "activities" },
      { emoji: "⭐", name: "star", keywords: ["star", "favorite", "rating", "excellence"], category: "symbols" },
      { emoji: "✨", name: "sparkles", keywords: ["sparkle", "magic", "shine", "special"], category: "symbols" },
      { emoji: "🔥", name: "fire", keywords: ["fire", "hot", "flame", "lit", "awesome"], category: "symbols" },
      { emoji: "💡", name: "light bulb", keywords: ["idea", "lightbulb", "innovation", "bright"], category: "objects" },
      { emoji: "📝", name: "memo", keywords: ["note", "write", "memo", "document", "text"], category: "objects" },
      { emoji: "📱", name: "mobile phone", keywords: ["phone", "mobile", "cell", "smartphone"], category: "objects" },
      { emoji: "💻", name: "laptop computer", keywords: ["laptop", "computer", "pc", "work"], category: "objects" },
      { emoji: "📊", name: "bar chart", keywords: ["chart", "graph", "data", "statistics", "analytics"], category: "objects" },
      { emoji: "📈", name: "chart increasing", keywords: ["chart", "graph", "growth", "increase", "success"], category: "objects" },
      { emoji: "📉", name: "chart decreasing", keywords: ["chart", "graph", "decline", "decrease", "loss"], category: "objects" },
      
      // Nature & Weather
      { emoji: "🌟", name: "glowing star", keywords: ["star", "glow", "bright", "special"], category: "nature" },
      { emoji: "🌙", name: "crescent moon", keywords: ["moon", "night", "lunar", "crescent"], category: "nature" },
      { emoji: "☀️", name: "sun", keywords: ["sun", "sunny", "bright", "day", "weather"], category: "nature" },
      { emoji: "⛅", name: "sun behind cloud", keywords: ["cloud", "sun", "partly cloudy", "weather"], category: "nature" },
      { emoji: "🌈", name: "rainbow", keywords: ["rainbow", "colorful", "pride", "hope"], category: "nature" },
      { emoji: "⚡", name: "high voltage", keywords: ["lightning", "electric", "power", "energy"], category: "nature" },
      { emoji: "🌊", name: "water wave", keywords: ["wave", "water", "ocean", "sea"], category: "nature" },
      { emoji: "🌺", name: "hibiscus", keywords: ["flower", "tropical", "bloom", "nature"], category: "nature" },
      { emoji: "🌸", name: "cherry blossom", keywords: ["flower", "pink", "spring", "bloom"], category: "nature" },
      { emoji: "🌿", name: "herb", keywords: ["plant", "green", "nature", "leaf"], category: "nature" },
      
      // Food & Drink
      { emoji: "☕", name: "hot beverage", keywords: ["coffee", "tea", "hot", "drink", "cafe"], category: "food" },
      { emoji: "🍕", name: "pizza", keywords: ["pizza", "food", "italian", "slice"], category: "food" },
      { emoji: "🍔", name: "hamburger", keywords: ["burger", "food", "fast food", "meat"], category: "food" },
      { emoji: "🍎", name: "red apple", keywords: ["apple", "fruit", "red", "healthy"], category: "food" },
      { emoji: "🥑", name: "avocado", keywords: ["avocado", "fruit", "green", "healthy"], category: "food" },
      { emoji: "🍰", name: "shortcake", keywords: ["cake", "dessert", "sweet", "strawberry"], category: "food" },
      { emoji: "🍪", name: "cookie", keywords: ["cookie", "dessert", "sweet", "snack"], category: "food" },
      { emoji: "🧊", name: "ice cube", keywords: ["ice", "cold", "frozen", "cube"], category: "food" },
      
      // Transport & Places
      { emoji: "🚀", name: "rocket", keywords: ["rocket", "space", "launch", "fast", "startup"], category: "transport" },
      { emoji: "✈️", name: "airplane", keywords: ["airplane", "plane", "flight", "travel"], category: "transport" },
      { emoji: "🚗", name: "automobile", keywords: ["car", "auto", "vehicle", "drive"], category: "transport" },
      { emoji: "🏠", name: "house", keywords: ["house", "home", "building", "residence"], category: "places" },
      { emoji: "🏢", name: "office building", keywords: ["office", "building", "work", "business"], category: "places" },
      { emoji: "🎯", name: "direct hit", keywords: ["target", "bullseye", "goal", "aim", "focus"], category: "activities" },
      
      // Symbols & Math
      { emoji: "✅", name: "check mark button", keywords: ["check", "done", "complete", "yes", "correct"], category: "symbols" },
      { emoji: "❌", name: "cross mark", keywords: ["no", "wrong", "error", "delete", "remove"], category: "symbols" },
      { emoji: "⚠️", name: "warning sign", keywords: ["warning", "caution", "alert", "danger"], category: "symbols" },
      { emoji: "ℹ️", name: "information", keywords: ["info", "information", "help", "about"], category: "symbols" },
      { emoji: "❓", name: "question mark", keywords: ["question", "help", "unknown", "ask"], category: "symbols" },
      { emoji: "❗", name: "exclamation mark", keywords: ["exclamation", "important", "alert", "notice"], category: "symbols" },
      { emoji: "🔢", name: "input numbers", keywords: ["numbers", "123", "math", "digits"], category: "symbols" },
      { emoji: "🔤", name: "input latin letters", keywords: ["letters", "abc", "alphabet", "text"], category: "symbols" },
      { emoji: "🆕", name: "NEW button", keywords: ["new", "fresh", "latest", "recent"], category: "symbols" },
      { emoji: "🆙", name: "UP! button", keywords: ["up", "increase", "level up", "improve"], category: "symbols" },
      { emoji: "🔝", name: "TOP arrow", keywords: ["top", "best", "peak", "highest"], category: "symbols" },
      { emoji: "🔜", name: "SOON arrow", keywords: ["soon", "coming", "future", "next"], category: "symbols" },
      
      // Additional useful emojis
      { emoji: "💰", name: "money bag", keywords: ["money", "cash", "rich", "wealth", "dollar"], category: "objects" },
      { emoji: "💎", name: "gem stone", keywords: ["diamond", "gem", "precious", "valuable"], category: "objects" },
      { emoji: "🔒", name: "locked", keywords: ["lock", "secure", "private", "protected"], category: "objects" },
      { emoji: "🔓", name: "unlocked", keywords: ["unlock", "open", "accessible", "free"], category: "objects" },
      { emoji: "🔑", name: "key", keywords: ["key", "password", "access", "unlock"], category: "objects" },
      { emoji: "⚙️", name: "gear", keywords: ["settings", "gear", "config", "tools", "mechanics"], category: "objects" },
      { emoji: "🛠️", name: "hammer and wrench", keywords: ["tools", "repair", "fix", "maintenance"], category: "objects" },
      { emoji: "📧", name: "e-mail", keywords: ["email", "mail", "message", "contact"], category: "objects" },
      { emoji: "📞", name: "telephone receiver", keywords: ["phone", "call", "contact", "communication"], category: "objects" },
      { emoji: "🎵", name: "musical note", keywords: ["music", "note", "song", "melody"], category: "symbols" },
      { emoji: "🎶", name: "musical notes", keywords: ["music", "notes", "song", "melody"], category: "symbols" },
      { emoji: "🔊", name: "speaker high volume", keywords: ["sound", "volume", "loud", "speaker"], category: "symbols" },
      { emoji: "🔇", name: "muted speaker", keywords: ["mute", "silent", "quiet", "no sound"], category: "symbols" }
    ];
  }

  createModeToggle() {
    // Create mode toggle buttons
    const modeToggle = document.createElement("div");
    modeToggle.className = "icon-picker-mode-toggle";
    modeToggle.innerHTML = `
      <button type="button" class="mode-btn active" data-mode="icons">
        <span>🎨</span> Icons
      </button>
      <button type="button" class="mode-btn" data-mode="emojis">
        <span>😀</span> Emojis
      </button>
    `;

    // Insert before the input container
    const inputContainer = this.searchInput.closest('.icon-picker-input');
    inputContainer.parentNode.insertBefore(modeToggle, inputContainer);

    // Add event listeners for mode toggle
    modeToggle.addEventListener("click", (e) => {
      if (e.target.matches(".mode-btn") || e.target.closest(".mode-btn")) {
        const btn = e.target.closest(".mode-btn");
        const mode = btn.dataset.mode;
        this.switchMode(mode);
        
        // Update button states
        modeToggle.querySelectorAll(".mode-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
      }
    });
  }

  switchMode(mode) {
    this.currentMode = mode;
    this.resultsDiv.innerHTML = "";
    this.searchInput.placeholder = mode === "emojis" ? "Search emojis..." : "Search icons...";
    
    // Update color picker visibility (emojis don't need color)
    if (this.colorPicker) {
      this.colorPicker.style.display = mode === "emojis" ? "none" : "block";
    }
    
    // Clear search input
    this.searchInput.value = "";
    this.selectedIcon.style.display = "block";
    this.selectedIcon.src = "";
    this.selectedIcon.textContent = "";
  }

  setupInitialIcon() {
    const currentValue = this.searchInput.value;
    if (currentValue) {
      if (this.isEmoji(currentValue)) {
        this.selectedIcon.style.display = "none";
        this.selectedIcon.textContent = currentValue;
      } else if (currentValue.endsWith(".svg")) {
        this.selectedIcon.style.display = "block";
        this.selectedIcon.src = `/${currentValue}`;
        this.selectedIcon.textContent = "";
      } else {
        this.selectedIcon.style.display = "block";
        this.selectedIcon.src = `https://api.iconify.design/${currentValue}.svg`;
        this.selectedIcon.textContent = "";
      }
    }
  }

  setupEventListeners() {
    this.searchInput.addEventListener("input", () => {
      const query = this.searchInput.value;
      if (query.length > 0) {
        if (this.currentMode === "emojis") {
          this.searchEmojis(query);
        } else {
          this.searchIcons(query);
        }
      } else {
        this.resultsDiv.innerHTML = "";
      }
    });

    this.form.addEventListener("submit", (event) => {
      if (this.savePath && this.currentMode === "icons") {
        this.downloadAndSaveSvg(
          `${this.icon}.svg&color=${this.colorPicker.value.replace("#", "%23")}`
        );
      }
      this.form.submit();
    });
  }

  isEmoji(text) {
    // Simple emoji detection - checks if text contains emoji characters
    const emojiRegex = /[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/u;
    return emojiRegex.test(text);
  }

  async searchIcons(query) {
    if (query.length < 3) {
      this.resultsDiv.innerHTML = "";
      return;
    }

    try {
      const response = await fetch(
        `https://api.iconify.design/search?query=${encodeURIComponent(
          query
        )}&limit=10&start=0&prefix=${this.selectedPrefix}`
      );
      const data = await response.json();

      this.resultsDiv.innerHTML = "";
      if (data.icons && data.icons.length > 0) {
        const dropdownList = document.createElement("div");
        dropdownList.className = "icon-dropdown-list";

        data.icons.forEach((icon) => {
          const color = this.colorPicker.value.replace("#", "%23");
          const iconBaseUrl = `https://api.iconify.design/${icon}.svg`;
          const iconUrl = `${iconBaseUrl}?color=${color}`;

          const dropdownItem = this.createIconDropdownItem(icon, iconUrl);
          dropdownList.appendChild(dropdownItem);
        });

        this.resultsDiv.appendChild(dropdownList);
      } else {
        this.resultsDiv.innerHTML = '<div class="no-results">No icons found.</div>';
      }
    } catch (error) {
      console.error("Error searching icons:", error);
      this.resultsDiv.innerHTML = '<div class="error">Error loading icons.</div>';
    }
  }

  searchEmojis(query) {
    const searchTerm = query.toLowerCase();
    const matches = this.emojiData.filter(item => 
      item.name.toLowerCase().includes(searchTerm) ||
      item.keywords.some(keyword => keyword.toLowerCase().includes(searchTerm)) ||
      item.emoji.includes(searchTerm)
    );

    this.resultsDiv.innerHTML = "";
    if (matches.length > 0) {
      const dropdownList = document.createElement("div");
      dropdownList.className = "emoji-dropdown-list";

      matches.slice(0, 20).forEach((emojiData) => {
        const dropdownItem = this.createEmojiDropdownItem(emojiData);
        dropdownList.appendChild(dropdownItem);
      });

      this.resultsDiv.appendChild(dropdownList);
    } else {
      this.resultsDiv.innerHTML = '<div class="no-results">No emojis found.</div>';
    }
  }

  createIconDropdownItem(icon, iconUrl) {
    const item = document.createElement("div");
    item.className = "icon-dropdown-item";

    const iconImg = document.createElement("img");
    iconImg.src = iconUrl;
    iconImg.className = "icon-preview";
    iconImg.alt = `Icon: ${icon}`;

    const iconText = document.createElement("span");
    iconText.textContent = icon;
    iconText.className = "icon-name";

    item.appendChild(iconImg);
    item.appendChild(iconText);

    item.addEventListener("click", () => {
      this.searchInput.value = icon;
      this.selectedIcon.style.display = "block";
      this.selectedIcon.src = iconUrl;
      this.selectedIcon.textContent = "";
      this.resultsDiv.innerHTML = "";
      this.icon = icon;
      
      if (this.savePath) {
        this.searchInput.value = `${this.savePath}/${this.model}/icon-${this.objectId}.svg`;
      } else {
        this.searchInput.value = icon;
      }
    });

    return item;
  }

  createEmojiDropdownItem(emojiData) {
    const item = document.createElement("div");
    item.className = "emoji-dropdown-item";

    const emojiSpan = document.createElement("span");
    emojiSpan.textContent = emojiData.emoji;
    emojiSpan.className = "emoji-preview";

    const emojiText = document.createElement("span");
    emojiText.textContent = emojiData.name;
    emojiText.className = "emoji-name";

    const emojiKeywords = document.createElement("span");
    emojiKeywords.textContent = emojiData.keywords.slice(0, 3).join(", ");
    emojiKeywords.className = "emoji-keywords";

    const textContainer = document.createElement("div");
    textContainer.className = "emoji-text-container";
    textContainer.appendChild(emojiText);
    textContainer.appendChild(emojiKeywords);

    item.appendChild(emojiSpan);
    item.appendChild(textContainer);

    item.addEventListener("click", () => {
      this.searchInput.value = emojiData.emoji;
      this.selectedIcon.style.display = "none";
      this.selectedIcon.textContent = emojiData.emoji;
      this.resultsDiv.innerHTML = "";
      this.icon = emojiData.emoji;
    });

    return item;
  }

  downloadAndSaveSvg(svgIcon) {
    const downloadUrl = `/icon_picker/download-svg/?icon=${svgIcon}&id=${this.objectId}&model=${this.model}`;
    fetch(downloadUrl)
      .then((response) => response.text())
      .then((data) => {
        this.searchInput.value = data;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}