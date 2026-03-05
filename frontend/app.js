const { useState } = React;

const App = () => {
  const [movie, setMovie] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState(null);

  const handleSearch = () => {

  if (!movie) return;

  setLoading(true);
  setResults([]);
  setError("");

  fetch(`http://127.0.0.1:5000/recommend?movie=${movie}`)
    .then((response) => response.json())
    .then((data) => {

      setLoading(false);

      if (data.error) {
        setResults([]);
        setError("No results found");
      } else {
        setResults(data.recommendations);
      }

    })
    .catch((error) => {

      console.error(error);
      setLoading(false);
      setResults([]);
      setError("Something went wrong");

    });
};

  return React.createElement(
    "div",
    { className: "container" },

    React.createElement("div", { className: "header" }, "Movie Recommender"),

    error && React.createElement("div", { className: "error-message" }, error),

    React.createElement(
      "div",
      { className: "search-container" },

      React.createElement(
        "div",
        { className: "search-row" },

        React.createElement("input", {
          className: "search-bar",
          placeholder: "Enter movie name...",
          value: movie,
          onChange: (e) => {
            const value = e.target.value;
            setMovie(value);

            if (value.length === 0) {
              setSuggestions([]);
              return;
            }

            fetch(`http://127.0.0.1:5000/search?query=${value}`)
              .then((res) => res.json())
              .then((data) => setSuggestions(data));
          },
        }),

        React.createElement(
          "button",
          {
            className: "button",
            onClick: handleSearch,
          },
          "Recommend",
        ),
      ),

      React.createElement(
        "div",
        { className: "suggestions" },

        suggestions.map((title, index) =>
          React.createElement(
            "div",
            {
              key: index,
              className: "suggestion-item",
              onClick: () => {
                setMovie(title);
                setSuggestions([]);
              },
            },
            title,
          ),
        ),
      ),
    ),

    loading
  ? React.createElement(
      "div",
      { className: "spinner" },
      "Loading recommendations..."
    )
  : React.createElement(
      "div",
      { className: "movies-grid" },

      results.map((movie, index) =>
        React.createElement(
          "div",
          {
            className: "movie-card",
            key: index,
            onClick: () => setSelectedMovie(movie)
          },

          React.createElement("img", {
            src: movie.poster
              ? movie.poster
              : "https://dummyimage.com/300x450/222/fff&text=No+Poster+Available",
            className: "poster",
            onError: (e) => {
              e.target.onerror = null;
              e.target.src =
                "https://dummyimage.com/300x450/222/fff&text=No+Poster+Available";
            }
          }),

          React.createElement("div", { className: "movie-title" }, movie.title)
        )
      )
    ),

selectedMovie &&
  React.createElement(
    "div",
    { className: "modal-overlay",
        onClick: () => setSelectedMovie(null)
     },

    React.createElement(
      "div",
      { className: "modal-content",
        onClick: (e) => e.stopPropagation()
      },

      React.createElement("img", {
        src: selectedMovie.poster || "./no-poster.png",
        className: "modal-poster"
      }),

      React.createElement(
        "div",
        { className: "modal-info" },

        React.createElement("h2", null, selectedMovie.title),

        React.createElement(
          "button",
          {
            className: "close-button",
            onClick: () => setSelectedMovie(null)
          },
          "Close"
        )
      )
    )
   )
  );
};

ReactDOM.render(React.createElement(App), document.getElementById("root"));
