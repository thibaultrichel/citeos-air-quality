import './navbar.css';

function Navbar() {
  return (
      <div className="nav-container">
          <img className="logo-citeos" src={require("./images/citeos.png")} width="215" height="48" alt={"Citeos"}/>
          <div className="title">CiteosVision</div>
          <img className="logo-esme" src={require("./images/esme.png")} width="80" height="80" alt="ESME Logo"/>
      </div>
  );
}

export default Navbar;
