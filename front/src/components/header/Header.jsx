import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import {RiPlantLine} from 'react-icons/ri';
import {FaUserAlt, FaLanguage} from 'react-icons/fa';
import {useTranslation} from 'react-i18next';
import {Link} from "react-router-dom";
import styles from './Header.module.scss';
import useAuth from '../../hooks/useAuth';

const Header = () => {
    const {t, i18n} = useTranslation();
    const {auth} = useAuth();

    function changeLanguage(language) {
        i18n.changeLanguage(language);
    }

    return (
        <Navbar sticky="top" bg="dark" variant="dark">
            <Container>
                <Navbar.Brand>
                    <Link to="/" style={{textDecoration: 'none', color: 'white'}}>
                        <RiPlantLine size={40}/> Laplanta
                    </Link>
                </Navbar.Brand>
                <Nav className="ml-auto">
                    <Nav.Item className={styles.profile}>
                        <NavDropdown title={
                            <span><FaLanguage size={30}/> {t("lang")}</span>
                            } onSelect={changeLanguage}>
                            <NavDropdown.Item eventKey="en">English</NavDropdown.Item>
                            <NavDropdown.Item eventKey="ua">Українська</NavDropdown.Item>
                        </NavDropdown>
                    </Nav.Item>
                    <Nav.Item className={styles.profile}>
                        <Link to="/profile" style={{textDecoration: 'none', color: 'white'}}>
                            <FaUserAlt size={18}/> 
                            {
                                auth?.email ? ` Welcome, ${auth.email}` 
                                : ` ${t("profile")}`
                            }
                        </Link>
                    </Nav.Item>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default Header;