import {useState, useEffect} from "react";
import useAxiosPrivate from '../../hooks/useAxiosPrivate';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {FaRegUserCircle} from 'react-icons/fa';
import {AiOutlineMail, AiOutlineCalendar, AiOutlineCheckCircle} from 'react-icons/ai';
import {BsTelephone} from 'react-icons/bs';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import ListGroup from 'react-bootstrap/ListGroup';
import {useNavigate, Link} from 'react-router-dom';
import useAuth from "../../hooks/useAuth";
import bg from '../../static/bg1.jpeg';
import chip from '../../static/chip.jpeg';
import ProgressBar from 'react-bootstrap/ProgressBar';
import {useTranslation} from 'react-i18next';

const Profile = () => {
    const {t} = useTranslation();
    const [user, setUser] = useState();
    const axiosPrivate = useAxiosPrivate();
    const navigate = useNavigate();
    const {setAuth} = useAuth();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();
        const getUser = async () => {
            try {
                const response = await axiosPrivate.get('/user', {
                    signal: controller.signal
                });
                isMounted && setUser(response.data?.msg?.user);
            } catch(e) {
                console.error(e);
            }
        }

        getUser();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, []);

    const logoutHandler = () => { 
        setAuth({});
        navigate("/login");
    }

    return (
        <div className="bg-light">
            <Container className="py-5">
                <Row>
                    <Col>
                        <ListGroup>
                            <ListGroup.Item className="text-center">
                                <FaRegUserCircle size={200} className='text-secondary'/>
                                <p className="text-muted mb-1">{user?.name}</p>
                                <p className="text-muted mb-4">{user?.email}</p>
                                <div className="d-flex justify-content-center mb-2">
                                    <Button onClick={logoutHandler} variant="outline-primary">{t("logout")}</Button>
                                </div>
                            </ListGroup.Item>
                        </ListGroup>
                        <br/>
                        <ListGroup>
                            <ListGroup.Item active className="d-flex justify-content-center align-items-center p-3">
                                <h4>{t("quick_summary")}</h4>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <p className="text-muted mb-1">{t("plants_status")}</p>
                                <ProgressBar variant="success" now={100} label={`100`}/>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <p className="text-muted mb-1">{t("sensors_status")}</p>
                                <ProgressBar variant="warning" now={100} label={`100`}/>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <p className="text-muted mb-1">{t("emergency_freq")}</p>
                                <ProgressBar variant="danger" now={99} label={`0.01`}/>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <p className="text-muted mb-1">{t("total_mark")}</p>
                                <ProgressBar now={98} label={`98`}/>
                            </ListGroup.Item>
                        </ListGroup>
                    </Col>
                    <Col lg="8">
                        <ListGroup>
                            <ListGroup.Item>
                                <Row>
                                    <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                                        <FaRegUserCircle size={20}/>
                                        <span className="p">{t("username")}</span>
                                    </Col>
                                    <Col sm="9" className="d-flex justify-content-start align-items-center">
                                        <span className="p text-muted">{user?.name}</span>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                                        <AiOutlineMail size={20}/>
                                        <span className="p">{t("email")}</span>
                                    </Col>
                                    <Col sm="9" className="d-flex justify-content-start align-items-center">
                                        <span className="p text-muted">{user?.email}</span>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                                        <BsTelephone size={20}/>
                                        <span className="p">{t("phone")}</span>
                                    </Col>
                                    <Col sm="9" className="d-flex justify-content-start align-items-center">
                                        <span className="p text-muted">{user?.telephone}</span>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                                        <AiOutlineCalendar size={20}/>
                                        <span className="p">{t("account_created")}</span>
                                    </Col>
                                    <Col sm="9" className="d-flex justify-content-start align-items-center">
                                        <span className="p text-muted">{user?.account_created}</span>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                                        <AiOutlineCheckCircle size={20}/>
                                        <span className="p">{t("confirmation_date")}</span>
                                    </Col>
                                    <Col sm="9" className="d-flex justify-content-start align-items-center">
                                        <span className="p text-muted">{user?.confirmation_date}</span>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <div className="d-flex justify-content-end mb-2 gap-3">
                                    <Button variant="primary" disabled>{t("edit")}</Button>
                                    <Button variant="outline-primary" disabled>{t("change_password")}</Button>
                                </div>
                            </ListGroup.Item>
                        </ListGroup>
                        <br/>
                        <Row>
                            <Col md="6">
                                <Card>
                                    <Card.Img variant="top" src={bg}/>
                                    <Card.Body>
                                        <Card.Title>{t("my_plants")}</Card.Title>
                                            <Card.Text>
                                                {t("currently_observed") + ": 0"}
                                            </Card.Text>
                                        <Button variant="primary">
                                            <Link to='/plants' className='text-light' style={{textDecoration: 'none'}}>
                                                {t("more_info")}
                                            </Link>
                                        </Button>
                                    </Card.Body>
                                </Card>
                            </Col>
                            <Col md="6">
                                <Card>
                                    <Card.Img variant="top" src={chip}/>
                                    <Card.Body>
                                        <Card.Title>{t("my_sensors")}</Card.Title>
                                            <Card.Text>
                                                {t("currently_connected") + ": 0"}
                                            </Card.Text>
                                        <Button variant="primary" disabled>{t("more_info")}</Button>
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default Profile;