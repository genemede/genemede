# GENEMEDE (GEneric NEuro MEtadata DEscriptors)

GENEMEDE is a generic metadata framework that may be used to comprehensively describe a neuroscience experiment.

## Organization

| file type | content |
| --- | --- |
| metadata_types | Templates for each of the categories. e.g. project_types.json contains metadata fields for the category "project". |
| metadata_databases | A list of dictionaries that contain instances of a particular category. e.g. projects.json may contain a list of projects all identifiable through their unique ID. Each of the instances follow the same structure as defined in project_types.json. |
| resource_files | Directory containing files such as technical manuals, datasheets, documents and other miscellaneous items that are referred to in the metadata descriptors. i.e. typically these files are linked using the 'resources' key. |
| metadata_properties | Directory containing json files that contain custom property values that may be unique to a particular category etc. Metadata descriptors may link to these files in order to load custom properties. |

## Overview

- The metadata are stored in the form of metadata json databases grouped into various high level categories. The high level categories are represented as categories.json or category_types.json.
- categories.json files are the metadata database containing instances of that particular category, this is a list of dict each with the below common structure.
  ```
  [
      {
          "guid": "",
          "datetime": "",
          "name": "",
          "description": "",
          "mtype": "project",
          "resources": {},
          "properties": {},
          "custom": {},
          "bids": {}
      }
  ]
  ```
- The category_types.json files contains the template used to create the instances above. Each of the properties are always described with the below common structure.
  ```
  "property_name": {
      "description": "",
      "levels": null,
      "units": null
      },
  ```
- Current high level categories are: `projects, ethics, fundings, subjects, researchers, sessions, studies, devices, and labs`. More will be added in the future.
- Below table describes each of the fields used in the common structure.

  | | |
  | --- | --- |
  | guid | globally unique ID |
  | datetime | date and time this entry was modified |
  | name | human readable name of the entry |
  | description | human readable description of the entry |
  | mtype | metadata type (of of a fixed list of mtypes allowed for an entity) | 
  | resources | place to include links to other files, URLs, and other entities.|
  | properties | List of key=value pairs that contain the metadata of interest for this entry. |
  | custom | custom key=value pairs that describe the entity and that do not belong anywhere else|
  | bids | List of key=value pairs as defined by BIDS specification. If a similar entry exists under properties, then an internal link to the particular entry under properties will be provided. OPTIONAL. |

- The metadata type `'mtype': "group_type"` denotes a collection of devices that have been assigned to a group. These include a minimum set of devices that have to be listed and described in terms of metadata when performing an experiment.
- Devices are broken down into suitably generic components. These components can then be listed as a `group` in order to form a device assembly. The individual components may then be interchanged with other devices, replaced etc.

## Linking between files
Currently we use the below conventions to refer to other entities within and in between the metadata databases. Links are always guids to other entries.

To refer to a project entry from within the projects.json from ethics.json, we can do the following,
```
"resources": {
	"project": "*guid.projects.json"
},
```
This is an asterisk `*` followed by the guid.category.json.

In order to refer to an entry from within the file, we use an asterisk followed by the field and the metadata key within separated by a period.
```
"bids": {
	"InstitutionName": "*properties.institute",
	"InstitutionAddress": "*properties.contact_address"
}
```