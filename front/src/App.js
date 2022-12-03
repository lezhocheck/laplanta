import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./App.scss";
import favicon from "./static/favicon.png";
import Header from './components/header/Header';
import Footer from './components/footer/Footer';
import CoverSection from './components/coversection/CoverSection';
import Blog from './components/blog/Blog';
import Container from 'react-bootstrap/Container';
import {Helmet} from 'react-helmet';
import './i18n/config';

function App() {
  return (
    <div className="application">
      <Helmet>
          <meta charSet="utf-8" />
          <title>Laplanta</title>
          <link rel="icon" href={favicon}/>
          <style>{"body { background-color: #212529; }"}</style>
      </Helmet>
      <Container className="App bg-dark" fluid>
        <Header/>
        <CoverSection/>
        <Blog/>
        <Footer/>
      </Container>
    </div>
  );
}

export default App;
