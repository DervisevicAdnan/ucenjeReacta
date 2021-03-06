function Square(props){
  return (
    <button 
      className="square" 
      onClick={props.onClick}
    >
      {props.value}
    </button>//
  );
}

class Board extends React.Component {
  

  renderSquare(i) {
    return <Square
      value={this.props.squares[i]}
      onClick={()=>this.props.onClick(i)}
    />;
  }

  render() {

    return (
      <div>
        <div className="status">{status}</div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}//

class Game extends React.Component {
  constructor(props){
    super(props);
    this.state={
      //squares: [], //Array(9).fill(null),
      history:[{
        squares: Array(9).fill(null),
      }],
      stepNumber: 0,
      xIsNext:true,
    };
  }

  componentDidMount() {
    fetch("/sabiranje?a=3&b=2")
      .then(res => res.text())
      .then(
        (result) => {
          console.log(result);
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          console.log(error);
        }
      )

    var eventSource = new EventSource("/stream/ticTacToe");
    eventSource.onmessage = (e) => {
      fetch("/api/ticTacToe")
      .then(response => response.json())
      .then(data => {this.setState({history : data.history, stepNumber : data.step});console.log(data);},error => console.log(error));
      /*fetch("/api/ticTacToeStep")
      .then(response => response.json())
      .then(data => {this.setState({stepNumber : data});console.log(data);},error => console.log(error));*/
    };

    fetch("/api/ticTacToe")
      .then(response => response.json())
      .then(data => {this.setState({history : data.history, stepNumber : data.step});console.log(data);},error => console.log(error));

    /*fetch("/api/ticTacToeStep")
      .then(response => response.json())
      .then(data => {this.setState({stepNumber : data});console.log(data);},error => console.log(error));*/
  }
//
  handleClick(i){
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    const current = history[history.length-1];
    const squares = current.squares.slice();
    //console.log(this.state.squares);
    console.log(squares)
    if(calculateWinner(squares)||squares[i]){
      return;
    }

    squares[i]=this.state.xIsNext ? 'X':'O';

    

    this.setState({
      history: history.concat([{
        squares:squares,
      }]),
      stepNumber: history.length,
      xIsNext: !this.state.xIsNext,
    });
    console.log(109);
    console.log(history);
    console.log(this.state.history);
    console.log(squares);
    console.log(current);
    console.log(109);
    const requestOptions = {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({"noviKorak":squares})
          };
          fetch('/api/noviKorak', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({history : data}),error => console.log(error));
  }

  jumpTo(step) {
    this.setState({
      stepNumber: step,
      xIsNext: (step % 2) === 0,
      
    });
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"setStep":step})
    };
    fetch('/api/ticTacToeSetStep', requestOptions)
      //.then(response => response.json())
      //.then(data => this.setState({history : data}),error => console.log(error));
  }

  render() {

    const history = this.state.history;
    const current = history[this.state.stepNumber];
    console.log(history);
    console.log("history");
    console.log(this.state.stepNumber);
    console.log(current);
    console.log(current.squares);
    const winner=false;//calculateWinner(current.squares);

    

    const moves = history.map((step, move) => {
      const desc = move ?
        'Go to move #' + move :
        'Go to game start';
      return (
        <li key={move}>
          <button onClick={() => this.jumpTo(move)}>{desc}</button>
        </li>
      );
    });

    let status;
    if(winner){
      status='Winner ' + winner;
    }else{
      status = 'Next player: ' + (this.state.xIsNext ? 'X':'O');
    }

    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={current.squares}
            onClick={i=>this.handleClick(i)}
          />
        </div>
        <div className="game-info">
          <div>{status}</div>
          <ol>{moves}</ol>
        </div>
        <Ulaz/>
        <ToDo/>
      </div>
    );
  }
}//

function calculateWinner(squares) {
  //console.log(squares);
  const lines = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6],
  ];
  for(let i=0; i<lines.length; i++){
    const [a,b,c]=lines[i];
    if(squares[a] && squares[a]===squares[b] && squares[a]===squares[c]) return squares[a];
  }
  return null;
}

class Ulaz extends React.Component{
  constructor(props){
    super(props);
    this.state={
      stanje: "nepoznato",
    };
  }
  render(){
    return(
      <div>
        <input type="text" name="tekst" id="tekst"/>
        <input type="button" value="Unesi" onClick={()=>{
          const requestOptions = {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ tekst: document.getElementById("tekst").value })
          };
          fetch('/api/novizapis', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({stanje : data.stanje}),error => console.log(error));
          
        }}/>
        <br/>
        <p>{this.state.stanje}</p>
      </div>
    );
  }
}

class ToDo extends React.Component{
  constructor(props){
    super(props);
    this.state={
      zad:[],
    };
  }

  componentDidMount() {
    var eventSource = new EventSource("/stream");
    eventSource.onmessage = (e) => {
      fetch("/api/to-do")
      .then(response => response.json())
      .then(data => {this.setState({zad : data});console.log(data);},error => console.log(error));
    };
    fetch("/api/to-do")
      .then(response => response.json())
      .then(data => {this.setState({zad : data});console.log(data);},error => console.log(error));
  }

  render(){
    const zadaci=this.state.zad.map(el => {
      return(
        <li key={el["id"]} className="lista" onClick={() => {
          const requestOptions = {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ izbaciZadatak: el["id"] })
          };
          fetch('/api/izbaci-zadatak', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({zad : data}),error => console.log(error));

        }}>
          {el["tekst"]}
        </li>
      );
    });//

    return(
      <div>
        <ul>
          {zadaci}
        </ul>
        <br/>
        <input type="text" name="noviZadatak" id="noviZadatak"/>
        <input type="button" value="Dodaj novi zadatak" onClick={() => {
          const requestOptions = {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ noviZadatak: document.getElementById("noviZadatak").value })
          };
          fetch('/api/novi-zadatak', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({zad : data}),error => console.log(error));

          document.getElementById("noviZadatak").value="";
        }}/>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);
