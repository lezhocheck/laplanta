import Badge from 'react-bootstrap/Badge';
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory from 'react-bootstrap-table2-paginator';
import Container from 'react-bootstrap/Container';
import {Link} from 'react-router-dom';
import ToolkitProvider, { Search } from 'react-bootstrap-table2-toolkit/dist/react-bootstrap-table2-toolkit';

const PlantTable = (props) => {
    const plants = props.plants.plants;
    const { SearchBar } = Search;

    const statusFormatter = (cell, row) => {
        return (
            <Badge pill bg="dark">
                {cell}
            </Badge>
        );
    }

    const nameFormetter = (cell, row) => {
        return (
            <Link>
                {cell}
            </Link>
        );
    }
      
    const columns = [
        {
            dataField: '_id',
            text: 'id',
            sort: true
        },
        {
            dataField: 'name',
            text: 'Name',
            formatter: nameFormetter,
            sort: true
        },
        {
            dataField: 'added_date',
            text: 'Added date',
            sort: true
        },
        {
            dataField: 'description',
            text: 'Description',
            sort: true
        },
        {
            dataField: 'status',
            text: 'Status',
            formatter: statusFormatter,
            sort: true
        }
    ];

    const pagination = paginationFactory({
        page: 2,
        sizePerPage: 5,
        sizePerPageList : [ {
            text: '5th', value: 5
          }, {
            text: '10th', value: 10
          }, {
            text: '20th', value: 20
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
                                <SearchBar { ...props.searchProps } />
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
                <h1>Data loading...</h1>    
            }
        </Container>
    );
}

export default PlantTable;