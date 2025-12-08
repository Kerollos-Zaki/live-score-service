import React, { useState, useEffect } from "react";
import "./App.css";

const App = () => {
  // 1. Initial Data
  const [matches, setMatches] = useState([
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
      homeScore: 1,        // Given them a score since it's 30 mins in
      awayScore: 0,
      time: "30'",         // Starts at 30
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
      time: "0'",          // Starts at 0
      status: "1st Half",
      isLive: true,
    },
  ]);

  // 2. Auto-Update Timer & Scores
  useEffect(() => {
    const timer = setInterval(() => {
      setMatches((prevMatches) =>
        prevMatches.map((match) => {
          if (match.isLive) {
            // 1. Increment Time
            let currentMin = parseInt(match.time);
            let newTime = match.time;
            
            if (currentMin < 90) {
              newTime = (currentMin + 1) + "'";
            }

            // 2. Random Goal Logic (Small chance to score)
            let newHomeScore = match.homeScore;
            let newAwayScore = match.awayScore;
            
            // 5% chance to score every tick (for demo purposes)
            if (Math.random() > 0.95) { 
               if (Math.random() > 0.5) newHomeScore += 1;
               else newAwayScore += 1;
            }

            return { 
              ...match, 
              time: newTime, 
              homeScore: newHomeScore, 
              awayScore: newAwayScore 
            };
          }
          return match;
        })
      );
    }, 1000); // Updates every 1 second (FAST MODE)

    return () => clearInterval(timer);
  }, []);

  const handleManualRefresh = () => {
    window.location.reload();
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo-container">
          <span className="soccer-icon">âš½</span>
          <h1>365Scores Match</h1>
        </div>
        
        <div className="header-actions">
          <button onClick={handleManualRefresh} className="refresh-btn">
            â†» Reset
          </button>
          <div className="live-badge">
            <span className="live-dot">â—</span> LIVE
          </div>
        </div>
      </header>

      <main className="match-grid">
        {matches.map((match) => (
          <MatchCard key={match.id} match={match} />
        ))}
      </main>
    </div>
  );
};

// Card Component
const MatchCard = ({ match }) => {
  const handleImageError = (e) => {
    e.target.src = "https://via.placeholder.com/60?text=Logo"; 
  };

  return (
    <div className={card ${match.isLive ? "live-card" : ""}}>
      <div className="card-header">
        {/* Shows Green text if Live */}
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
          <div className={score-box ${match.isLive ? "live-border" : ""}}>
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
