import Badge from 'react-bootstrap/Badge';
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory from 'react-bootstrap-table2-paginator';
import Container from 'react-bootstrap/Container';
import {Link} from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';
import ToolkitProvider, { Search } from 'react-bootstrap-table2-toolkit/dist/react-bootstrap-table2-toolkit';
import {useTranslation} from 'react-i18next';

const PlantTable = (props) => {
    const {t} = useTranslation();
    const plants = props.plants.plants;
    const { SearchBar } = Search;

    const statusFormatter = (cell, row) => {
        return (
            <Badge pill bg="dark">
                {cell}
            </Badge>
        );
    }

    const idFormetter = (cell, row) => {
        const route = `/plant/${cell}`;
        return (
            <Link to={route}>
                {cell}
            </Link>
        );
    }
      
    const columns = [
        {
            dataField: '_id',
            text: 'id',
            formatter: idFormetter,
            sort: true
        },
        {
            dataField: 'name',
            text: t("plant_name"),
            sort: true
        },
        {
            dataField: 'added_date',
            text: t("added_date"),
            sort: true
        },
        {
            dataField: 'description',
            text: t("description"),
            sort: true
        },
        {
            dataField: 'status',
            text: t("status"),
            formatter: statusFormatter,
            sort: true
        }
    ];

    const pagination = paginationFactory({
        page: 1,
        sizePerPage: 5,
        sizePerPageList : [ {
            text: '5', value: 5
          }, {
            text: '10', value: 10
          }, {
            text: '20', value: 20
          } ]
    });


    return (
        <Container>
            {
                plants && plants.length > 0 
                ?
                <ToolkitProvider
                    bootstrap4 
                    keyField="_id"
                    data={plants}
                    columns={columns}
                    search>
                    {
                        props => (
                        <div>
                            <div className='d-flex justify-content-end'>
                                <SearchBar placeholder={t("search")} srText={t("search_in_plants")}  { ...props.searchProps }/>
                            </div>
                            <hr/>   
                            <BootstrapTable
                                { ...props.baseProps }
                                pagination={ pagination }
                                bordered={false}
                            />
                        </div>
                        )
                    }
                    </ToolkitProvider>
                :
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            }
        </Container>
    );
}

export default PlantTable;