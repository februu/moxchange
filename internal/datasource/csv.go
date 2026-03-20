package datasource

import (
	"encoding/csv"
	"os"
)

type CSVDataSource struct {
	Path   string
	file   *os.File
	reader *csv.Reader
}

func NewCSVDataSource(path string, skipHeader bool) (*CSVDataSource, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}

	r := csv.NewReader(f)

	if skipHeader {
		_, err := r.Read()
		if err != nil {
			return nil, err
		}
	}

	return &CSVDataSource{
		Path:   path,
		file:   f,
		reader: r,
	}, nil
}

func (c *CSVDataSource) Next() ([]string, error) {
	record, err := c.reader.Read()
	if err != nil {
		return nil, err
	}
	return record, nil
}

func (c *CSVDataSource) Close() error {
	if c.file != nil {
		return c.file.Close()
	}
	return nil
}
