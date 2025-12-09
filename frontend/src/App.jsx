import React, { useState, useEffect } from "react";
import "./App.css";

const App = () => {
  // 1. Initial Data (The 3 Hardcoded Matches)
  const initialMatches = [
    {
      id: 1,
      homeTeam: "Al Ahly",
      awayTeam: "Zamalek",
      homeLogo: "/assets/ahly.png",
      awayLogo: "/assets/zamalek.png",
      homeScore: 0,
      awayScore: 0,
      time: "0'",
      status: "1st Half",
      isLive: true,
    },
    {
      id: 2,
      homeTeam: "Bayern",
      awayTeam: "Dortmund",
      homeLogo: "https://crests.football-data.org/5.png",
      awayLogo: "https://crests.football-data.org/4.png",
      homeScore: 1,
      awayScore: 0,
      time: "30'",
      status: "1st Half",
      isLive: true,
    },
    {
      id: 3,
      homeTeam: "AC Milan",
      awayTeam: "Inter",
      homeLogo: "https://crests.football-data.org/98.png",
      awayLogo: "https://crests.football-data.org/108.png",
      homeScore: 0,
      awayScore: 0,
      time: "0'",
      status: "1st Half",
      isLive: true,
    },
  ];

  // --- SEPARATE STATES ---
  // One state for your 3 local matches, one state for matches from Python
  const [localMatches, setLocalMatches] = useState(initialMatches);
  const [backendMatches, setBackendMatches] = useState([]);

  // --- HELPER: LOGO MAPPING ---
  const getLogo = (name) => {
    if (name === "Al Ahly") return "/assets/ahly.png";
    if (name === "Zamalek") return "/assets/zamalek.png";
    if (name === "Bayern") return "https://crests.football-data.org/5.png";
    if (name === "Dortmund") return "https://crests.football-data.org/4.png";
    if (name === "AC Milan") return "https://crests.football-data.org/98.png";
    if (name === "Inter") return "https://crests.football-data.org/108.png";
    if (name === "Liverpool") return "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg";
    if (name === "Man United") return "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg";
    if (name === "Real Madrid") return "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg";
    if (name === "Barcelona") return "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg";
    if (name === "Chelsea") return "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg";
    if (name === "Arsenal") return "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg";
    return "https://via.placeholder.com/60?text=Logo";
  };

  // --- FETCH BACKEND MATCHES ---
  const fetchBackendMatches = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/matches");
      if (response.ok) {
        const backendData = await response.json();
        
        // Format them to match your design
        const formatted = backendData.map(m => ({
          id: m.match_id,
          homeTeam: m.home_team,
          awayTeam: m.away_team,
          homeLogo: getLogo(m.home_team),
          awayLogo: getLogo(m.away_team),
          homeScore: m.home_score,
          awayScore: m.away_score,
          time: m.minute || "0'",
          status: m.is_live ? "1st Half" : "Finished",
          isLive: m.is_live
        }));

        setBackendMatches(formatted);
      }
    } catch (error) {
      console.error("Failed to fetch matches:", error);
    }
  };

  // --- TIMER EFFECT (Only affects Local Matches) ---
  useEffect(() => {
    const timer = setInterval(() => {
      setLocalMatches((prev) => 
        prev.map(match => {
          if (match.isLive) {
            let currentMin = parseInt(match.time);
            if (currentMin < 90) {
              return { ...match, time: (currentMin + 1) + "'" };
            }
          }
          return match;
        })
      );
    }, 1000); // Fast mode: updates every 1 second
    return () => clearInterval(timer);
  }, []);

  // --- SYNC EFFECT (Only affects Backend Matches) ---
  useEffect(() => {
    fetchBackendMatches();
    const interval = setInterval(fetchBackendMatches, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleManualRefresh = () => {
    fetchBackendMatches();
  };

  // Combine them for the UI
  const allMatches = [...localMatches, ...backendMatches];

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo-container">
          <span className="soccer-icon">⚽</span>
          <h1>365Scores Match</h1>
        </div>
        
        <div className="header-actions">
          <button onClick={handleManualRefresh} className="refresh-btn">
            ↻ Reset
          </button>
          <div className="live-badge">
            <span className="live-dot">●</span> LIVE
          </div>
        </div>
      </header>

      <main className="match-grid">
        {allMatches.map((match) => (
          <MatchCard key={match.id} match={match} />
        ))}
      </main>
    </div>
  );
};


// Card Component (Unchanged)
const MatchCard = ({ match }) => {
  const handleImageError = (e) => {
    e.target.src = "https://via.placeholder.com/60?text=Logo"; 
  };

  return (
    <div className={`card ${match.isLive ? "live-card" : ""}`}>
      <div className="card-header">
        <span className={match.isLive ? "match-time live-text" : "match-time"}>
          {match.time}
        </span>
        <span className="match-status">{match.status}</span>
      </div>

      <div className="card-body">
        <div className="team">
          <img 
            src={match.homeLogo} 
            alt={match.homeTeam} 
            className="team-logo"
            onError={handleImageError} 
          />
          <span className="team-name">{match.homeTeam}</span>
        </div>

        <div className="scoreboard">
          <div className={`score-box ${match.isLive ? "live-border" : ""}`}>
            {match.homeScore} - {match.awayScore}
          </div>
        </div>

        <div className="team">
          <img 
            src={match.awayLogo} 
            alt={match.awayTeam} 
            className="team-logo"
            onError={handleImageError} 
          />
          <span className="team-name">{match.awayTeam}</span>
        </div>
      </div>
    </div>
  );
};

export default App;
