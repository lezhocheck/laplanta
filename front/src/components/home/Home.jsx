import Header from '../header/Header';
import Footer from '../footer/Footer';
import CoverSection from '../coversection/CoverSection';
import Login from '../auth/Login';
import Signup from '../auth/Signup';
import Blog from '../blog/Blog';

const Home = () => {
    return (
        <div>
            <Header/>
            <Signup/>
            <Footer/>
        </div>
    );
}

export default Home;